# YouTube Trend Dashboard
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-071D49?logo=Python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-00A3E0?logo=OpenAI&logoColor=white)](https://openai.com/)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FmadEffort%2Fyoutube-trend-dashboard&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=round)](https://makeapullrequest.com)

This web application is used for analyzing and comparing popular YouTube video trends and comments, enabling users to gain insights into topics that can garner high views or optimal upload times. It utilizes the YouTube Data API v3 to fetch rankings of popular videos from various countries and provides features such as upload patterns and sentiment analysis of video comments.

The application is developed primarily in Python and relies on the Pandas library for data processing and analysis. Sentiment analysis of YouTube comments is performed using a pretrained model (`matthewburke/korean_sentiment`). Additionally, the OpenAI API is utilized for interpreting complex data analysis results and providing meaningful insights. Streamlit library is used to provide an intuitive and user-friendly web interface.

> (Beta Version) Added feature to determine if specific videos are suitable for children by checking the frequency of profanity in the comments.

## Table of Contents
1. [Introduction](#introduction)
2. [Structure](#structure)
3. [Design Pattern](#design-pattern)
4. [Brief Feature Overview](#brief-feature-overview)
5. [Installation Guide](#installation-guide)
6. [How to Use](#how-to-use)
7. [Feature Showcase and Explanation](#feature-showcase-and-explanation)
8. [Technologies Used](#technologies-used)
9. [Information and License](#information-and-license)

## Introduction
**YouTube Trend Dashboard** provides an easy way to grasp the latest YouTube trends and helps users find optimal upload times and topics to garner more views. Users can increase their chances of success on YouTube by planning content aligned with trends and uploading strategies. Choosing the right topic and upload timing are crucial factors for success on YouTube. This dashboard provides practical data and analysis to optimize these aspects.

## Structure
```
📦src
 ┣ 📂config
 ┃ ┣ 📜analysis_options.py
 ┃ ┣ 📜country_code.py
 ┃ ┗ 📜page_config.py
 ┣ 📂controllers
 ┃ ┗ 📜controller.py
 ┣ 📂models
 ┃ ┗ 📜model.py
 ┣ 📂utils
 ┃ ┣ 📜echart_generator.py
 ┃ ┣ 📜loading.py
 ┃ ┗ 📜sentiment_analysis.py
 ┣ 📂views
 ┃ ┗ 📜view.py
 ┗ 📜main.py
```

## Design Pattern
- **Model:**
  - In `model.py`, data is fetched from the YouTube Data API to provide video data to the rest of the application. It also handles data processing and analysis, including additional logic such as sentiment analysis (`sentiment_analysis.py`).
- **View:**
  - `view.py` is responsible for constructing the user interface using Streamlit, fetching data from the model based on user input, and visualizing the data received.
- **Controller:**
  - `controller.py` requests data from the model based on user input, processes the data, and passes it to the view. It centralizes logic for handling user input.

## Brief Feature Overview
- **Country Selection:** Users can select a country to view popular YouTube videos from that region.
- **Popular Video Analysis:** Displays a dashboard of popular videos with sorting and paging functionalities.
- **Analysis Features:** Options for analyzing upload ratios by day or time, average tag count in popular videos, etc.
- **Word Cloud Visualization:** Generates a word cloud of popular video titles to provide visual insights into common topics or keywords.
- **YouTube Comment Analysis:** Analyzes sentiments (positive/negative) of comments on specific videos.
- **Interactive Interface:** Provides a conversational interface using Streamlit for easy exploration of various analyses and visualizations.
- **YouTube Comparison:** Compares information between two YouTube videos.

## Installation Guide
1. Clone the repository
```
git clone https://github.com/madEffort/youtube-trend-dashboard.git
```
2. Create a virtual environment
3. Install required packages
```
poetry install
```
4. Create a `.env` file and set environment variables
```
YOUTUBE_API_KEY="*********************"
OPEN_API_KEY="***********************"
```
5. Run the application
```
streamlit run src/main.py
```


## How to Use
After running the application, navigate through the interactive sidebar on the left to explore different features:
- Select a country to view popular YouTube videos.
- Choose analysis options and click on "Run Analysis" to execute the analysis.
- Click on "Generate Word Cloud" to create a word cloud visualization.
- Input a YouTube video ID and click on "Analyze" to perform sentiment analysis on the comments.
- Input two YouTube video IDs and click on "Compare" to compare and visualize information about the two videos.

## Feature Showcase and Explanation

### YouTube Analysis
<table>
  <tr>
    <td colspan=2>
      <br>
      <b>Analysis Method: Popular Video Upload Ratio by Weekday</b><br>
      <br>
    </td>
  </tr>
  <tr>
	  <td align="center" width="50%">
		  <img src="images/example-1.gif" alt="Analysis Method: Popular Video Upload Ratio by Weekday" width="600" height="335" />
	  </td>
	  <td>
		  ➡ We provide weekday-wise popular video upload information from Monday to Sunday and utilize the OpenAI API to analyze it, recommending the best upload days for maximizing views. <br><br>
		  ➡ While loading, we utilize a third-party library from Streamlit to present users with a loading animation.<br><br>
	  </td>
</table>
<table>
  <tr>
    <td colspan=2>
      <br>
      <b>Analysis Method: Popular Video Upload Ratio by Time Slots</b><br>
      <br>
    </td>
  </tr>
  <tr>
	  <td align="center" width="50%">
		  <img src="images/example-2.gif" alt="Analysis Method: Popular Video Upload Ratio by Time Slots" width="600" height="335" />
	  </td>
	  <td>
		  ➡ We offer popular video upload information categorized by time slots and utilize the OpenAI API to analyze it, recommending optimal time slots for maximizing views.
	  </td>
</table>
<table>
  <tr>
    <td colspan=2>
      <br>
      <b>Analysis Method: Average Number of Tags Used in Popular Videos</b><br>
      <br>
    </td>
  </tr>
  <tr>
	  <td align="center" width="50%">
		  <img src="images/example-3.gif" alt="Analysis Method: Average Number of Tags Used in Popular Videos" width="600" height="335" />
	  </td>
	  <td>
		  ➡ We calculate the average number of tags used in the Top 200 popular videos on YouTube and provide this information. It serves as a guide for users on how many tags to use when uploading a video.
	  </td>
</table>
<table>
  <tr>
    <td colspan=2>
      <br>
      <b>Analysis Method: Word Cloud Generation</b><br>
      <br>
    </td>
  </tr>
  <tr>
	  <td align="center" width="50%">
		  <img src="images/example-4.gif" alt="Analysis Method: Word Cloud Generation" width="600" height="335" />
	  </td>
	  <td>
		  ➡ We visualize and recommend popular topics and keywords on YouTube for the selected country.
	  </td>
</table>

### YouTube Comment Analysis
<table>
  <tr>
    <td colspan=2>
      <br>
      <b>YouTube Comment Analysis</b><br>
      <br>
    </td>
  </tr>
  <tr>
	  <td align="center" width="50%">
		  <img src="images/example-5.gif" alt="YouTube Comment Analysis" width="600" height="335" />
	  </td>
	  <td>
		  ➡ The system takes the video ID as input and analyzes the comments for the corresponding YouTube video. It provides the user with the ratio of positive and negative reactions in the comments.<br><br>
      ➡ (Beta Version) Child-Friendly Content Assessment Feature: It counts the occurrences of profanity in the video to determine whether the content is suitable for children to watch, and notifies the user accordingly.
	  </td>
</table>

### YouTube Comparison
<table>
  <tr>
    <td colspan=2>
      <br>
      <b>YouTube Comparison</b><br>
      <br>
    </td>
  </tr>
  <tr>
	  <td align="center" width="50%">
		  <img src="images/example-6.gif" alt="YouTube Comparison" width="600" height="335" />
	  </td>
	  <td>
		  ➡ The user inputs two YouTube video IDs, and visualizes and compares the information of the provided videos.<br><br>
      	➡ The user can compare views, likes, comments, tags used, upload date and day, and audience reactions (comments) for the videos at a glance.
	  </td>
</table>

## Technologies Used
- **Python:** Core programming language of the project
- **Streamlit:** Used to create the web application
- **Pandas:** Utilized for data manipulation and analysis
- **Sentiment Analysis:** Pretrained model (matthewburke/korean_sentiment) used to classify comments into positive or negative sentiments
- **YouTube Data API v3:** Fetches data on popular videos and comments from YouTube
- **Echarts and WordCloud:** Employed for data visualization
- **YouTubeTranscriptApi:** Used to fetch YouTube subtitles (Beta Version)
- **OpenAI API:** Utilized for interpreting complex data analysis results and providing insights
  
This project follows the Model-View-Controller (MVC) architectural design pattern.

## Information and License

This project adheres to the Apache-2.0 license, and you can find more detailed information in the [LICENSE](https://github.com/madEffort/youtube-trend-dashboard/blob/main/LICENSE) file.
