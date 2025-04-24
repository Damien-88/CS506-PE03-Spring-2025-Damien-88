import bs4
import requests
import openpyxl

htrefs = {} # Dictionary to store links & their titles
res = requests.get("https://news.ycombinator.com/news") # Get the Hacker News page

# Check if request was successful
try:
    res.raise_for_status() # Raise an error if request failed
    soup = bs4.BeautifulSoup(res.text, "html.parser") # Parse HTML content
    links = soup.select("span.titleline > a") # Select all links in titleline

    # Iterate through each link & store its text & href in dictionary
    for link in links:
        # Check if link has href attribute
        if link.get("href") is not None:
            htrefs.update({link.get_text(): link.get("href")}) # Add link text & href to dictionary
    
    # Print each link & its title
    for h in htrefs:
        print(f"{h}\n{htrefs[h]}\n")

    # Create new Excel workbook & sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Hacker News Links"

    ws.append(["Title", "Link"]) # Add header row

    # Add rows
    for ht in htrefs:
        ws.append([ht, htrefs[ht]])

    # Save workbook
    wb.save("Hacker_News_Links.xlsx") # Save to file

    # Write to text file
    with open("Hacker_News_Links.txt", "w") as f:
        for htr in htrefs:
            if list(htrefs.keys()).index(htr) == len(htrefs) - 1:
                f.write(f"{htr}\n{htrefs[htr]}")
            else:
                f.write(f"{htr}\n{htrefs[htr]}\n\n") # Write each link & its title

# If request failed, print error
except Exception as exc:
    print(f"There was a problem: {exc}")