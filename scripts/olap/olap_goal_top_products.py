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


def analyze_top_products_by_region(cube_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify the top-selling products by region and month, based on total sales.
    """
    try:
        # Rename for clarity
        cube_df = cube_df.rename(columns={"sale_amount_sum": "total_sales"})

        # Sort descending by total sales
        sorted_df = cube_df.sort_values(by=["region", "Month", "total_sales"], ascending=[True, True, False])

        # Group by region and month ONLY, then take top 3
        top_products = sorted_df.groupby(["region", "Month"]).head(3).reset_index(drop=True)

        logger.info("Top-selling products by region and month identified successfully.")
        return top_products
    except Exception as e:
        logger.error(f"Error identifying top products by region: {e}")
        raise


def visualize_top_products_by_region(top_products: pd.DataFrame) -> None:
    """Visualize the top-selling product by region and month."""
    try:
        # Plot: grouped bar by region + month
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_products, x="region", y="total_sales", hue="product_name", palette="viridis")

        plt.title("Top-Selling Products by Region and Month")
        plt.xlabel("Region")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the visualization
        output_path = RESULTS_OUTPUT_DIR.joinpath("top_products_by_region_month.png")
        plt.savefig(output_path)
        logger.info(f"Visualization saved to {output_path}.")
        plt.show()
    except Exception as e:
        logger.error(f"Error visualizing top products by region: {e}")
        raise


def main():
    """Main function for analyzing and visualizing top-selling products by region and month."""
    logger.info("Starting TOP_PRODUCTS_BY_REGION analysis...")

    # Step 1: Load the precomputed OLAP cube
    cube_df = load_olap_cube(CUBED_FILE)

    # Step 2: Analyze top products by region
    top_products = analyze_top_products_by_region(cube_df)

    # Step 3: Save top products as CSV
    top_csv = RESULTS_OUTPUT_DIR.joinpath("top_products_by_region_month.csv")
    top_products.to_csv(top_csv, index=False)
    logger.info(f"Top products by region saved to {top_csv}.")

    # Step 4: Visualize top products
    visualize_top_products_by_region(top_products)

    logger.info("Analysis and visualization of top-selling products completed successfully.")

if __name__ == "__main__":
    main()