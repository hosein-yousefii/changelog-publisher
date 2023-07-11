import os
import sys
import markdown2
from jinja2 import Environment
import requests

"""
[Usage]
These variable can be replaced:

ChangeLogGen_htmlOutputToFile       OPTIONAL    You are able to save the converted html file. (default: true)
ChangeLogGen_changeLogTemplate      OPTIONAL    You can have your own changelog template (default: ./ChangeLogTemplate.md)
ChangeLogGen_ChangeLogFile          REQUIRED    Path to the Changelog.md (default: ./CHANGELOG.md)
ChangeLogGen_htmlFile               REQUIRED    Converted changelog to html. (default: CHANGELOG.html)
ChangeLogGen_headerTag              REQUIRED    Header tag which is used in changelog template. (default: [header])
ChangeLogGen_footerTag              REQUIRED    Footer tag which is used in changelog template. (default: [footer])
ChangeLogGen_confluenceURL          REQUIRED    Confluence url.(default: http://lkwconfluence.lkw-walter.com)
ChangeLogGen_confluenceSpace        REQUIRED    Cofluence space which you want to create/update the page.
ChangeLogGen_confluencePageTitle    REQUIRED    Confluence page which you want to put your changelog.
ChangeLogGen_confluenceApiKey       REQUIRED    Confluence api key.

You don't need to specify ariables with default value.
"""

changeloghtml_outputToFile = os.environ.get('ChangeLogGen_htmlOutputToFile','true')
changeLogTemplate_filePath = os.environ.get('ChangeLogGen_changeLogTemplate', 'ChangeLogTemplate.md')
changeLog_filePath = os.environ.get('ChangeLogGen_changeLogFile', 'CHANGELOG.md')
changeLogHtml_filePath = os.environ.get('ChangeLogGen_htmlFile', 'CHANGELOG.html')
start_string = os.environ.get('ChangeLogGen_headerTag','[header]')
end_string = os.environ.get('ChangeLogGen_footerTag','[footer]')
confluence_url = os.environ.get('ChangeLogGen_confluenceURL', 'http://confluence-server.com')
confluence_space = os.environ.get('ChangeLogGen_confluenceSpace', 'DEVOPS')
confluence_pageTitle = os.environ.get('ChangeLogGen_confluencePageTitle', 'test-application')
confluence_apiKey = os.environ.get('ChangeLogGen_confluenceApiKey', 'TEST')

if not os.path.exists(changeLog_filePath):
  print(f"[ERROR]: The {changeLog_filePath} doesn't exist, make sure to run git-changelog first.")
  sys.exit()

if os.path.exists(changeLogHtml_filePath):
  print(f"[ERROR]: The {changeLogHtml_filePath} is already exist.")
  sys.exit()

# Read change log template to extract header and footer
def read_content_between_strings(changeLogTemplate_filePath, start_string, end_string):

  if not os.path.isfile(changeLogTemplate_filePath):
    print("[ERROR]:Path is not a file:", changeLogTemplate_filePath)
    return 1

  if not os.access(changeLogTemplate_filePath, os.R_OK):
    print("[ERROR]: File is not readable:", changeLogTemplate_filePath)
    return 1

  with open(changeLogTemplate_filePath, 'r') as file:
    content = file.read()

    start_index = content.lower().find(start_string)
    end_index = content.lower().find(end_string)
    if end_string == "end_of_file":
      end_index = None

    if start_index == -1 or end_index == -1:
      print("[ERROR]: File should contain '[Header] and [Footer] tag' Header or Footer string not found in the file.")
      return 1

  start_index += len(start_string)

  extracted_content = content[start_index:end_index].strip()

  return extracted_content

# convert created changelog to html format
def convert_to_html(changeLog_filePath,changeLogHtml_filePath):
  if not os.path.exists(changeLog_filePath):
    print("[ERROR]: File does not exist:", changeLog_filePath)
    return 1

  if not os.path.isfile(changeLog_filePath):
    print("[ERROR]:Path is not a file:", changeLog_filePath)
    return 1

  if not os.access(changeLog_filePath, os.W_OK):
    print("[ERROR]: File is not readable:", changeLog_filePath)
    return 1

  with open(changeLog_filePath, 'r+') as file:
    file_content = file.read()

  html_content = markdown2.markdown(file_content)

  template_code = """
  {{ html_content }}
  """
  # Create the Jinja2 environment
  env = Environment()

  # Render the template code with the data
  changeLogHtmlConverted = env.from_string(template_code).render(html_content=html_content)
  return changeLogHtmlConverted

# add extracted header and footer to Changelog file.
def add_header_footer(changeLogHtmlConverted,header_content,footer_content):

  htmlOpenTag = "<h4>"
  htmlCloseTag = "</h4>"

  changelog_with_header_footer = htmlOpenTag + header_content.replace("\n","</h4>\n<h4>") + htmlCloseTag
  changelog_with_header_footer += changeLogHtmlConverted
  changelog_with_header_footer += htmlOpenTag + footer_content.replace("\n","</h4>\n<h4>") + htmlCloseTag

  print("[INFO]: Header and footer added successfully!")
  return changelog_with_header_footer

# Make html compatible with confluence structure
def compatible_to_confluence(newChangeLog_file,changeLogHtml_filePath):
  # define confluence html  macro format
  changeLogConfluenceCompatible = "<ac:structured-macro ac:name='html' ac:schema-version='1' ac:macro-id='cf730d54-5751-4cec-9461-28c790b9fc37'><ac:plain-text-body><![CDATA["
  confluenceHtmlFooter="]]></ac:plain-text-body></ac:structured-macro>"
  changeLogConfluenceCompatible += newChangeLog_file.replace("\"","'") + confluenceHtmlFooter

  # Save the output to an HTML file
  if changeloghtml_outputToFile.lower() == 'true':
    with open(changeLogHtml_filePath, "w") as file:
      file.write(changeLogConfluenceCompatible)

  print("[INFO]: markdown file successfuly converted to html")
  return changeLogConfluenceCompatible

# Upload generated document to a confluence page
def upload_to_confluence(changeLogConfluenceCompatible,confluence_apiKey, confluence_pageTitle, confluence_url, confluence_space):

  # Server availability
  url = confluence_url + "/rest/api"
  try:
    response = requests.head(url)
  except:
      print(f"[ERROR]: Confluence is not reachable, check if the url is correct: {url}")
      return 1

  # Authorization check
  headers = {"Authorization": f"Bearer {confluence_apiKey}"}
  url = confluence_url + "/rest/api/space?limit=1&status=archived"
  try:
    response = requests.get(url, headers=headers)
    data = response.json()
    if data["results"] == []:
        print(f"[ERROR]: You're not authorised, make sure the confluence api key is correct.")
        return 1
  except requests.RequestException as e:
    print(f"[ERROR]: An error occurred: {e}")

  # Check if page exist to decide create new one or update it.
  url = confluence_url + "/rest/api/content"
  params = {"title": confluence_pageTitle,"spaceKey": confluence_space,"expand": "history"}

  try:
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    headers = {"Authorization": f"Bearer {confluence_apiKey}", "Content-Type": "application/json"}

    # Create new page if it doesn't exist.
    if data["results"] == []:
      data = {
        "type": "page",
        "title": confluence_pageTitle,
        "space": {
          "key": confluence_space
        },
        "body": {
          "storage": {
            "value": changeLogConfluenceCompatible,
            "representation": "storage"
          }
        }
      }

      try:
        response = requests.post(url, headers=headers, json=data)
      except:
        print(f"[ERROR]: Couldn't create the page: {confluence_pageTitle}")
        return 1

      print(f"[INFO]: Page {confluence_pageTitle} created successfuly.")

    # Update the page if exist.
    else:
      page_id = data["results"][0]["id"]
      url =  url = confluence_url + f"/rest/api/content/{page_id}"

      # gather the current version of the page
      try:
          response = requests.get(url, headers=headers)
      except:
          print(f"[ERROR]: Couldn't fetch page ({confluence_pageTitle}) version.")
          return 1

      data = response.json()
      version = data["version"]["number"] + 1

      # Update the page with new data
      data = {
        "id": page_id,
        "type": "page",
        "title": confluence_pageTitle,
        "space": {
          "key": confluence_space
        },
        "body": {
          "storage": {
            "value": changeLogConfluenceCompatible,
            "representation": "storage"
          }
        },
        "version": {
          "number": version
        }
      }

      try:
        response = requests.put(url, headers=headers, json=data)
      except:
        print(f"[ERROR]: Couldn't update the page: {confluence_pageTitle}")
        return 1

    linkToPage= confluence_url + f"/display/{confluence_space}/{confluence_pageTitle}"
    print(f"[INFO]: Page {confluence_pageTitle} updated successfuly.")
    print(f"[INFO]: Find this page here: {linkToPage}")

  except:
    print(f"[ERROR]: Cannot get information about this page: {confluence_pageTitle}, you can make sure if the inputs are correct: space={confluence_space}, params={params}")
    return 1

header_content = read_content_between_strings(changeLogTemplate_filePath, start_string, end_string)
footer_content = read_content_between_strings(changeLogTemplate_filePath, end_string, "end_of_file")

changeLogHtmlConverted = convert_to_html(changeLog_filePath,changeLogHtml_filePath)
newChangeLog_file = add_header_footer(changeLogHtmlConverted,header_content,footer_content)
changeLogConfluenceCompatible = compatible_to_confluence(newChangeLog_file,changeLogHtml_filePath)

upload_to_confluence(changeLogConfluenceCompatible,confluence_apiKey, confluence_pageTitle, confluence_url, confluence_space)
