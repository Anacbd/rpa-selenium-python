# 🚀 RPA Web Automation with Python & Selenium

This project is a Robotic Process Automation (RPA) system developed for the **Software Testing and Automation** course. The goal is to demonstrate automated filling of complex web forms using both dynamic and persistent data strategies.

## 📋 Features

The project covers two main automation approaches:

* **Dataset-Driven Automation (`mock1.py`):** Handles form filling using a fixed dataset from a CSV file generated via *Mockaroo*.
* **Dynamic Data Generation (`mock2.py`):** Leverages the **Faker** library to generate realistic, random data (names, emails, dates) in real-time, removing external file dependencies.
* **Evidence Management:** The bot automatically clears previous result folders and captures screenshots of the success screen after every submission.
* **Resilience:** Implementation of *Explicit Waits* and JavaScript-based clicks to handle slow network conditions and UI overlays (like ads).

## 🛠️ Technologies Used

* **Python 3.x**
* **Selenium WebDriver:** Browser interaction automation.
* **Pandas:** Data manipulation and CSV reading.
* **Faker:** Synthetic realistic data generation.
* **WebDriver Manager:** Automatic browser driver management.

## 🔧 How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/python-selenium-faker-rpa.git](https://github.com/your-username/python-selenium-faker-rpa.git)
