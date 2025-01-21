import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Tong's Daily Dose", layout="centered")

# Embed the HTML content
html_code = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Tong's Daily Dose</title>
    <style>
      :root {
        --light-pink: #f7ebe8;
        --dark-brown: #5c4033;
        --light-beige: #efeae4;
        --soft-orange: #f8d9c4;
        --warm-orange: #edbfa6;
      }
      body {
        font-family: "Arial", sans-serif;
        margin: 0;
        padding: 0;
        background-color: var(--light-beige);
        color: var(--dark-brown);
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      header {
        background-color: var(--light-pink);
        padding: 2rem;
        text-align: center;
        border-bottom: 2px solid var(--dark-brown);
        width: 100%;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        color: var(--dark-brown);
      }
      header h1 {
        font-size: 2.5rem;
        font-family: "Georgia", serif;
        margin: 0;
      }
      header p {
        font-size: 1.2rem;
        color: var(--dark-brown);
      }
      nav {
        margin: 2rem 0;
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: center;
      }
      nav a {
        font-size: 1rem;
        color: white;
        text-decoration: none;
        padding: 0.8rem 1.5rem;
        border-radius: 20px;
        background-color: var(--dark-brown);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, background-color 0.3s;
      }
      nav a:hover {
        background-color: var(--soft-orange);
        transform: scale(1.05);
      }
      .content {
        margin: 2rem;
        padding: 1.5rem;
        background: var(--light-pink);
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        width: 90%;
        max-width: 800px;
        color: var(--dark-brown);
      }
      .content h2 {
        font-family: "Georgia", serif;
        color: var(--dark-brown);
        font-size: 2rem;
        margin-bottom: 1rem;
      }
      .content p {
        font-size: 1.1rem;
        line-height: 1.8;
        color: var(--dark-brown);
      }
      footer {
        text-align: center;
        background-color: var(--light-pink);
        color: var(--dark-brown);
        padding: 1.5rem 0;
        margin-top: auto;
        width: 100%;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
      }
      footer p {
        margin: 0;
        font-size: 0.9rem;
      }
    </style>
  </head>
  <body>
    <header>
      <h1>Tong's Daily Dose</h1>
      <p>Documenting my learning journey, one step at a time.</p>
    </header>

    <nav>
      <a href="#daily" onclick="showPage('daily')">Daily Dose ☕</a>
      <a href="#weekly" onclick="showPage('weekly')">Weekly Wrap-ups</a>
      <a href="#resources" onclick="showPage('resources')">Resources</a>
    </nav>

    <div id="daily" class="content">
      <h2>Daily Dose ☕</h2>
      <p>Select a date to explore daily entries:</p>
      <ul>
        <li>
          <a href="#daily-21012025" onclick="showPage('daily-21012025')">21.01.2025</a>
        </li>
      </ul>
    </div>

    <div id="daily-21012025" class="content" style="display: none">
      <h2>Daily Dose ☕ - 21.01.2025</h2>
      <p>
        今天開始344天的15分鐘小記錄. 今天跟朋友coffee chat學到組織一個完整的report然後最喜歡朋友下的一句話
        "讓他們瞧瞧你有多厲害" 最喜歡這種guts! 然後跟一位DS犯蠢發現自己的bug根本就差在一個S.
        然後脫離git desktop :D! 開啟自己的專案:D 每天準時收看Tong的Daily Dose !
      </p>
    </div>

    <div id="weekly" class="content" style="display: none">
      <h2>Weekly Wrap-ups</h2>
      <p>Summarize my week's progress and highlights.</p>
    </div>

    <div id="resources" class="content" style="display: none">
      <h2>Resources</h2>
      <p>List helpful articles, videos, or books here.</p>
    </div>

    <footer>
      <p>&copy; 2025 Tong's Daily Dose. All rights reserved.</p>
    </footer>

    <script>
      function showPage(pageId) {
        const pages = document.querySelectorAll(".content");
        pages.forEach((page) => (page.style.display = "none"));
        document.getElementById(pageId).style.display = "block";
      }
    </script>
  </body>
</html>
"""

# Display the HTML code using Streamlit's components
st.components.v1.html(html_code, height=800, scrolling=True)
