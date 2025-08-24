# 🧮 Advanced Calculator Pro - A Feature-Rich Streamlit Application

 <!-- Optional: Replace with a URL to a screenshot of your app -->

A comprehensive, multi-functional calculator application built with Python and Streamlit. This app provides a clean, responsive, and user-friendly interface for various calculation needs, from simple arithmetic to complex scientific functions, programming conversions, and data analysis.

## ✨ Features

This application is divided into five powerful modes:

-   **Scientific Calculator:** A fully-featured scientific calculator with standard arithmetic, trigonometric functions (`sin`, `cos`, `tan`), logarithms (`ln`, `log`), powers (`x²`, `xʸ`), roots (`√`), factorials (`n!`), and constants (`π`, `e`).
-   **Programmer Calculator:** Instantly convert integers between Decimal, Hexadecimal, and Binary. Perform bitwise operations (`AND`, `OR`, `XOR`, `NOT`).
-   **Unit Converters:**
    -   **Currency:** Real-time exchange rates using a public API.
    -   **Physical Units:** Convert Length, Mass, Temperature, and Data Storage with a responsive keypad.
-   **Data Analysis:** Input a list of numbers (via pasting or keypad entry) to get key statistics (Mean, Median, Std Dev) and a histogram to visualize the data distribution.
-   **Graphing Calculator:** Plot one or more mathematical functions on an interactive graph. Supports `numpy` functions for complex plotting.

## 🛠️ Built With

-   **Python 3**
-   **Streamlit:** For creating the interactive web application UI.
-   **NumPy:** For numerical operations and data analysis.
-   **Matplotlib:** For plotting graphs and histograms.
-   **Pint:** For handling physical unit conversions with high accuracy.
-   **Requests:** For making API calls to fetch real-time currency data.

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You need to have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1.  **Clone the repository:**
    ```
    git clone https://github.com/your-username/advanced-calculator-pro.git
    cd advanced-calculator-pro
    ```

2.  **Create and activate a virtual environment (recommended):**
    -   On Windows:
        ```
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required packages:**
    A `requirements.txt` file is included to install all necessary libraries at once.
    ```
    pip install -r requirements.txt
    ```

### Running the Application

Once the installation is complete, you can run the app with a single command:

