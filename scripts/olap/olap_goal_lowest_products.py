import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import sys
import seaborn as sns

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger  # noqa: E402

# Constants
OLAP_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("olap_cubing_outputs")
CUBED_FILE: pathlib.Path = OLAP_OUTPUT_DIR.joinpath("multidimensional_olap_cube.csv")
RESULTS_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("results")

# Create output directory for results if it doesn't exist
RESULTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_olap_cube(file_path: pathlib.Path) -> pd.DataFrame:
    """Load the precomputed OLAP cube data."""
    try:
        cube_df = pd.read_csv(file_path)
        logger.info(f"OLAP cube data successfully loaded from {file_path}.")
        return cube_df
    except Exception as e:
        logger.error(f"Error loading OLAP cube data: {e}")
        raise


def analyze_worst_products_by_region(cube_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify the lowest-selling product in each region based on total sales.
    """
    try:
        # Sort by year, region, and total sales ascending
        sorted_df = cube_df.sort_values(by=["Year", "region", "sale_amount_sum"], ascending=[True, True, True])

        # Rename sale_amount_sum
        sorted_df.rename(columns={"sale_amount_sum": "total_sales"}, inplace=True)

        # Get the bottom product per year and region
        lowest_products = sorted_df.groupby(["Year", "region", "product_name"]).head(3).reset_index(drop=True)

        logger.info("Lowest-selling products by region identified successfully.")
        return lowest_products
    except Exception as e:
        logger.error(f"Error identifying lowest-selling products by region: {e}")
        raise


def visualize_lowest_products_by_region(lowest_products: pd.DataFrame) -> None:
    """Visualize the lowest-selling products by region and year."""
    try:
        # Plot: grouped bar by region + year
        plt.figure(figsize=(10, 6))
        sns.barplot(data=lowest_products, x="region", y="total_sales", hue="Year", hue_order=sorted(lowest_products["Year"].unique()), palette="Reds")

        plt.title("Lowest-Selling Products by Region and Year", fontsize=16)
        plt.xlabel("Region")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the visualization
        output_path = RESULTS_OUTPUT_DIR.joinpath("lowest_products_by_region_year.png")
        plt.savefig(output_path)
        logger.info(f"Visualization saved to {output_path}.")
        plt.show()
    except Exception as e:
        logger.error(f"Error visualizing lowest-selling products by region: {e}")
        raise


def main():
    """Main function for analyzing and visualizing worst-selling products by region and year."""
    logger.info("Starting LOWEST_PRODUCTS_BY_REGION_YEAR analysis...")

    # Step 1: Load the precomputed OLAP cube
    cube_df = load_olap_cube(CUBED_FILE)

    # Step 2: Analyze lowest-selling products by region
    lowest_products = analyze_worst_products_by_region(cube_df)

    # Step 3: Save lowest products as CSV
    low_csv = RESULTS_OUTPUT_DIR.joinpath("lowest_products_by_region_year.csv")
    lowest_products.to_csv(low_csv, index=False)
    logger.info(f"Lowest-selling products by region saved to {low_csv}.")

    # Step 4: Visualize lowest products
    visualize_lowest_products_by_region(lowest_products)

    logger.info("Analysis and visualization of bottom-selling products completed successfully.")

if __name__ == "__main__":
    main()