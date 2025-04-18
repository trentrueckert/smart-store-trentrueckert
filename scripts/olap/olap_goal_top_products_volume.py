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

def analyze_top_products_by_volume(cube_df: pd.DataFrame) -> pd.DataFrame:
    """Identify the most frequently sold products in each region (by sale count), drilled down by year and month."""
    try:
        # Sort by year, month, region, and sale count descending
        sorted_df = cube_df.sort_values(by=["Year", "Month", "region", "sale_id_count"], ascending=[True, True, True, False])

        # Get top 3 products per year-region-month by count
        top_volume = sorted_df.groupby(["Year", "Month", "region", "product_name"]).head(3).reset_index(drop=True)

        logger.info("Top products by volume identified successfully.")
        return top_volume
    except Exception as e:
        logger.error(f"Error analyzing top products by volume: {e}")
        raise


def visualize_top_products_by_sales_count(top_volume_products: pd.DataFrame) -> None:
    """Visualize the top 3 selling products by sales count using a grouped bar chart with a year → month drilldown."""
    try:
        plt.figure(figsize=(10, 6))

        # Create a grouped bar chart by year and month
        sns.barplot(data=top_volume_products, x="Month", y="sale_id_count", hue="product_name", palette="Set2", ci=None)

        # Set labels and title
        plt.title("Top 3 Selling Products by Sales Count (Month-wise within Year)", fontsize=16)
        plt.xlabel("Month")
        plt.ylabel("Sales Count")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the grouped bar chart
        output_path = RESULTS_OUTPUT_DIR.joinpath("top_products_by_sales_count_month.png")
        plt.savefig(output_path)
        logger.info(f"Top products by sales count grouped bar chart saved to {output_path}.")
        plt.show()
    except Exception as e:
        logger.error(f"Error visualizing top products by sales count: {e}")
        raise


def visualize_sale_counts_heatmap(cube_df: pd.DataFrame) -> None:
    """Visualize total number of sales across regions and years using a heatmap."""
    try:
        heatmap_data = cube_df.groupby(["region", "Year", "Month"])["sale_id_count"].sum().unstack(level=["Year", "Month"])

        # Sort years (columns) in ascending order
        heatmap_data = heatmap_data[sorted(heatmap_data.columns)]

        plt.figure(figsize=(10, 6))
        sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlOrBr", linewidths=0.5, vmin=0)

        plt.title("Total Number of Sales by Region and Year")
        plt.xlabel("Year")
        plt.ylabel("Region")
        plt.tight_layout()

        output_path = RESULTS_OUTPUT_DIR.joinpath("sales_heatmap_region_year.png")
        plt.savefig(output_path)
        logger.info(f"Sales heatmap saved to {output_path}.")
        plt.show()
    except Exception as e:
        logger.error(f"Error generating sales heatmap: {e}")
        raise


def main():
    """Main function for analyzing and visualizing sale count by region and year using a grouped bar chart and heatmap."""
    logger.info("Starting SALE_COUNT_BY_REGION_YEAR analysis...")

    # Step 1: Load the precomputed OLAP cube
    cube_df = load_olap_cube(CUBED_FILE)

    # Step 2: Analyze top-selling products by volume (sale count)
    top_volume_products = analyze_top_products_by_volume(cube_df)

    # Step 3: Save top-volume products as CSV
    top_volume_csv = RESULTS_OUTPUT_DIR.joinpath("top_volume_products_by_region_year.csv")
    top_volume_products.to_csv(top_volume_csv, index=False)
    logger.info(f"Top volume products saved to {top_volume_csv}.")

    # Step 4: Visualize top-selling products by sales count using a grouped bar chart
    visualize_top_products_by_sales_count(top_volume_products)

    # Step 5: Visualize sale counts via heatmap using the full cube data
    visualize_sale_counts_heatmap(cube_df)

    logger.info("Grouped bar chart and heatmap analysis of sale counts completed successfully.")

if __name__ == "__main__":
    main()