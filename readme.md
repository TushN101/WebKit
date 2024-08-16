# Website Tool Kit

## Overview

The Website Tool Kit is a project aimed at providing a set of tools for website security assessments. Currently, the repository is under development and will be populated with various features designed to enhance web security.

## Features

- **Subdirectory Finder (In Progress):** A tool to detect and list subdirectories within a website.
- **Subdomain Finder (Planned):** A tool to identify and enumerate subdomains associated with a website.
- **Payload Creator (Planned):** A tool to generate custom payloads for security testing purposes.

## Installation

Follow these steps to set up and run WebKit:

1. **Clone the Repository**

   Use Git to clone the repository to your local machine:
   ```
   git clone https://github.com/TushN101/WebKit.git
   ```

2. **Navigate to the Project Directory**

   Change into the project directory:
   ```
   cd WebKit
   ```

3. **Install Dependencies**

   Install the required Python libraries using `pip`. This project requires the `requests` library:
   ```
   pip install requests
   ```


4. **Run the Application**

   Start the application by executing the main script:
   ```
   python core.py
   ```

## Usage

1. **Choose a Website**

   Select the website you want to analyze. Enter the website URL into the tool as instructed in the application.


2. **Run the Tool**

   Let the tool process the website to detect subdirectories, identify subdomains, or generate payloads, depending on the feature you are using. The tool will display the results on your screen.

   ![pic2](https://github.com/user-attachments/assets/5248c053-c47c-489b-ade6-ff786087cd9d)

3. **View Cached Results**

   The tool caches the results of your scan in a JSON file for future reference. This allows for quick access to previously obtained data without having to re-run the scan.

   ![pic3](https://github.com/user-attachments/assets/b4dbd76f-463b-4aa1-b5ce-f1b8534e3301)

   You can view or clear the cached results by accessing the `cache.json` file in the project directory.


## Contributing

Contributions are welcome. Please check back later for contribution guidelines.

## Authors

- Tushar N
- Raahim Shaikh
- Neal Parmar
- Arshad Shaikh
