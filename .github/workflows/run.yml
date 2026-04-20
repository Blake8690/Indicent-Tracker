name: Run Python script

on:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.9"

      - name: Install packages
        run: |
          pip install requests python-dateutil

      - name: Run script
        run: |
          python send_email.py
