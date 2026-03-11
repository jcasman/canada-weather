"""
Sales Data Visualization Tutorial
Reads CSV data and displays it in a bar chart using flet-charts
"""

import flet as ft
from flet_charts import BarChart, BarChartGroup, BarChartRod, ChartAxis, ChartAxisLabel


def read_csv(filename: str) -> list[dict]:
    """
    Read a CSV file and return a list of dictionaries.

    Each dictionary contains:
    - "month": month name
    - "snow": snowfall in cm
    - "temperature": average temperature in °C
    """
    data = []

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        # Skip the header line (first line)
        for line in lines[1:]:
            # Remove newline and any extra whitespace
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Split by comma and use tuple unpacking
            month, snow_str, temp_str = line.split(",")

            # Extract and convert values
            month = month.strip()
            snow = int(snow_str.strip())
            temperature = int(temp_str.strip())

            # Store in dictionary
            data.append({"month": month, "snow": snow, "temperature": temperature})

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return []
    except ValueError as e:
        print(f"Error: Could not parse data - {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

    return data


def create_sales_chart(data: list[dict]) -> BarChart:
    """
    Create a bar chart from the Alberta climate data.

    Shows snowfall (cm) and temperature (°C) as side-by-side bars for each month.
    """
    groups = []
    bottom_labels = []

    # Y-axis must include both snow (0 to max cm) and temperature (can be negative °C)
    min_temp = min(item["temperature"] for item in data)
    max_snow = max(item["snow"] for item in data)
    max_val = max(max_snow, max(item["temperature"] for item in data))
    min_val = min(0, min_temp)
    # Round axis bounds for clean labels
    max_y = ((max_val // 5) + 1) * 5
    min_y = ((min_val // 5) - 1) * 5 if min_val < 0 else 0

    for index, item in enumerate(data):
        # Use first 3 letters of month name for x-axis label
        month_short = item["month"][:3]

        # Snow bar: always from 0 upward
        snow_from = 0
        snow_to = item["snow"]
        # Temperature bar: from 0 to value (can be negative)
        temp_from = min(0, item["temperature"])
        temp_to = max(0, item["temperature"])

        # Create a group with two bars: snowfall and temperature
        group = BarChartGroup(
            x=index,
            rods=[
                # Snowfall bar (blue)
                BarChartRod(
                    from_y=snow_from,
                    to_y=snow_to,
                    color=ft.Colors.BLUE_400,
                    width=25,
                    tooltip=f"Snowfall: {item['snow']} cm",
                ),
                # Temperature bar (red/orange)
                BarChartRod(
                    from_y=temp_from,
                    to_y=temp_to,
                    color=ft.Colors.ORANGE_400,
                    width=25,
                    tooltip=f"Temperature: {item['temperature']} °C",
                ),
            ],
            spacing=4,
        )
        groups.append(group)
        bottom_labels.append(ChartAxisLabel(value=index, label=month_short))

    # Y-axis labels: span negative (temp) and positive (snow)
    left_labels = []
    step = 5
    value = min_y
    while value <= max_y:
        if value == 0:
            label_text = "0"
        else:
            label_text = str(value)
        left_labels.append(ChartAxisLabel(value=value, label=ft.Text(label_text)))
        value += step

    chart = BarChart(
        groups=groups,
        group_spacing=12,
        width=900,
        height=450,
        margin=ft.Margin.only(left=24),
        left_axis=ChartAxis(
            labels=left_labels,
            label_size=18,
            label_spacing=12,
        ),
        bottom_axis=ChartAxis(title=ft.Text("Month"), labels=bottom_labels),
    )

    return chart


def calculate_totals(data: list[dict]) -> dict:
    """Calculate total snowfall and average temperature."""
    total_snow = sum(item["snow"] for item in data)
    avg_temp = sum(item["temperature"] for item in data) / len(data) if data else 0

    return {"total_snow": total_snow, "avg_temp": avg_temp}


def main(page: ft.Page):
    """Main function to set up and run the Flet app."""
    page.title = "Alberta Climate Data"
    page.padding = 30
    page.scroll = "auto"

    # Read data from CSV file
    data = read_csv("data.csv")

    if not data:
        # Show error message if no data loaded
        page.add(
            ft.Text(
                "Error: Could not load data from CSV file.",
                color=ft.Colors.RED,
                size=18,
            )
        )
        return

    # Calculate totals
    totals = calculate_totals(data)

    # Create chart
    chart = create_sales_chart(data)

    # Build the UI
    page.add(
        # Title
        ft.Text(
            "Monthly Snowfall and Temperature — Alberta, Canada",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        ),
        # Summary statistics
        ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        f"Total Snowfall: {totals['total_snow']} cm",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.BLUE_700,
                    ),
                    ft.Text(
                        f"Average Temperature: {totals['avg_temp']:.1f} °C",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.ORANGE_700,
                    ),
                ],
                spacing=30,
            ),
            margin=ft.Margin.only(bottom=20),
        ),
        # Chart
        ft.Container(
            content=chart,
            padding=20,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=10,
        ),
        # Legend
        ft.Row(
            [
                ft.Container(
                    width=20, height=20, bgcolor=ft.Colors.BLUE_400, border_radius=4
                ),
                ft.Text("Snowfall (cm)", size=14),
                ft.Container(width=30),
                ft.Container(
                    width=20, height=20, bgcolor=ft.Colors.ORANGE_400, border_radius=4
                ),
                ft.Text("Temperature (°C)", size=14),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            margin=ft.Margin.only(top=20),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
