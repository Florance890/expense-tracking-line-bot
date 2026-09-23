# 花草帳 — Expense Tracking LINE Bot

A conversational expense-tracking LINE Bot built with Python and Flask for recording and reviewing everyday spending.

## Overview

花草帳 is a small LINE Bot project that turns simple chat messages into expense records. Users can enter an item and amount, review records, check totals, request help, and query records by date. Expense data is separated by LINE user ID so different users can maintain independent records.

## Core Features

- Add an expense with a simple message such as `午餐 120`
- View today's expense records with `查看`
- Check today's total with `總額`
- View help instructions with `幫助`
- Query a date using `MM/DD` format
- Keep expense records separated by LINE user ID
- Validate input format, numeric amounts, and positive values

## Tech Stack

- Python
- Flask
- LINE Messaging API
- REST API requests
- JSON file storage

## Project Structure

```text
expense-tracking-line-bot/
├── app.py
├── test_webhook.py
├── expenses.example.json
├── requirements.txt
├── .env.example
├── .gitignore
└── assets/
```

## How It Works

1. LINE sends a message event to the Flask `/webhook` endpoint.
2. The bot reads the message and LINE user ID.
3. `handle_message()` determines whether the message is a command, a date query, or a new expense.
4. Expense records are stored in a local JSON file and grouped by user ID.
5. The bot replies through the LINE Reply API.

## Local Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the environment variable used by the bot:

```text
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
```

Then run:

```bash
python app.py
```

> Do not commit a real LINE access token or private user data to GitHub. `expenses.json` is intentionally excluded by `.gitignore`.

## Testing & Debugging

The project was tested across core usage scenarios including expense entry, record viewing, total calculation, date queries, help instructions, and use by another LINE account. Debugging was an important part of the development process.

`test_webhook.py` is retained as an early local webhook test script from development. Its simplified payload does not reproduce the complete LINE Messaging API event structure used by the final webhook.

## Future Improvements

- Replace local JSON storage with a database
- Improve webhook handling for multiple events
- Add richer weekly, monthly, and yearly spending summaries
- Add calendar/reminder features
- Expand automated tests using realistic LINE event payloads

## Notes

This repository is a cleaned public version of the original project. Personal expense data and LINE user IDs are not included.
