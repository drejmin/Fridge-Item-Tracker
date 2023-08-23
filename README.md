# Fridge-Item-Tracker

# FORGET ME NOT by Repo Depot

## Project Idea and descriptions

This project is to help remind forgetful folks when their perishables are expiring and send helpful notifications (in the form of emails) prior to the date of expiration and/or prior to garbage day. We hope everyone can now have a better budgeted life after being influenced by our app!

## API/technologies/npm packages

- Python3
- Django
- HTML
- CSS
- JS

## ERDs

![](https://hackmd.io/_uploads/BkIFsnt2h.png)

## Restful Routing Chart

| HTTP Verb | URL Path         | Action         | Description                                            |
| --------- | ---------------- | -------------- | ------------------------------------------------------ |
| GET       | /receipts        | index          | Retrieve a list of all receipts                        |
| GET       | /receipts/:id    | show           | Retrieve a specific receipt by ID                      |
| POST      | /receipts        | create         | Create a new receipt                                   |
| PUT       | /receipts/:id    | update         | Update an existing receipt by ID                       |
| PATCH     | /receipts/:id    | partial update | Update part of an existing receipt by ID (optional)    |
| DELETE    | /receipts/:id    | destroy        | Delete a specific receipt by ID                        |
| GET       | /perishables     | index          | Retrieve a list of all perishables                     |
| GET       | /perishables/:id | show           | Retrieve a specific perishable by ID                   |
| POST      | /perishables     | create         | Create a new perishable                                |
| PUT       | /perishables/:id | update         | Update an existing perishable by ID                    |
| PATCH     | /perishables/:id | partial update | Update part of an existing perishable by ID (optional) |
| DELETE    | /perishables/:id | destroy        | Delete a specific perishable by ID                     |
| GET       | /reminders       | index          | Retrieve a list of all reminders                       |
| GET       | /reminders/:id   | show           | Retrieve a specific reminder by ID                     |
| POST      | /reminders       | create         | Create a new reminder                                  |
| PUT       | /reminders/:id   | update         | Update an existing reminder by ID                      |
| PATCH     | /reminders/:id   | partial update | Update part of an existing reminder by ID (optional)   |
| DELETE    | /reminders/:id   | destroy        | Delete a specific reminder by ID                       |

## Wireframes of all user views

![Wireframe1](https://i.imgur.com/wio0Rzy.png)
![Wireframe2](https://i.imgur.com/PzFfw2n.png)

## User Stories

### AAU(As a user):

- I want to be able to import receipts
- I want to see a list of all purchased items
- I want to see a list of expired items
- I want to receive a reminder the day before the item is to expire
- I want to be able to comment and chat with other users about purchased items

## MVP goals

- [x] Setup django boilerplate
- [x] Setup django superadmins
- [x] Setup django auth and users
- [x] Update models.py
  - [x] reminders
  - [ ] perishables
  - [x] receipts
- [x] Update views.py
  - [x] reminders
  - [x] perishables
  - [x] receipts
- [x] Setup urls.py
  - [x] reminders
  - [x] perishables
  - [x] receipts
- [x] Register models to admin.py
  - [x] reminders
  - [x] perishables
  - [x] receipts
- [x] Add template views for:
  - [x] reminders
  - [x] perishables
  - [x] receipts
- [x] Connect to S3 to hold receipt images
- [x] Email Reminders

## Stretch Goals

- Create a chat to communicate with fellow refrigerator mates on how to ingest perishing items
  - Connect with api:
    - Quilljs api for rich text formatting
    - emojidata.ai api
- Connect with an OCR (Optical Character Recognition) api
  - https://ocr.space/receiptscanning
  - https://tabscanner.com/
  - Google Cloud Vision API
  - AWS Textract
  - Microsoft Azure Computer Vision API
  - Tesseract (Open Source)
  - ABBYY Cloud OCR SDK
    -Add dynamic refrigerator graphic to homepage

## Contributers

- Deandre (https://github.com/drejmin)
- Amanda (https://github.com/amandaputney)
- Paul (https://github.com/LeepDev)
