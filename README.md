# [spamofthetimes.com](https://spamofthetimes.com)

![Screenshot of a chart entitled 'spam of the times' showing the count of spam texts received per day betwen September 2022 and February 2024](https://raw.githubusercontent.com/scottleechua/spam-of-the-times/main/assets/header_spamofthetimes.png)

Interactive demo / dataviz for my [public dataset](https://github.com/scottleechua/data/tree/main/spam-and-marketing-sms) `spam-and-marketing-sms`, which contains every text message I've received since September 2022.

## Development
Requires [Make](https://www.gnu.org/software/make/) and [Poetry](https://python-poetry.org/) 2.1 or higher.
- `make setup` to install dependencies and pre-commit hooks
- `make dev` to run the web app locally

## Tech stack
- Web app created with [Plotly](https://plotly.com/python/getting-started/) + [Dash](https://dash.plotly.com/).
- Deployed on [Google Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run) with [continuous deployment from this repo using Cloud Build](https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build).
- Cookieless analytics with [GoatCounter](https://github.com/arp242/goatcounter).

## Acknowledgements
Thanks to Xiu Ting Foong for the website name!

## Contribute
For bug reports or features, please open an issue before making a pull request.

## License

This repo, excluding ***website content***, is made available under the [MIT License](/LICENSE), where website content is defined as
- the prose writing in [`app.py`](/app.py), e.g., text in `<p>`, `<ol>`, and `<a>` elements; and
- this `README`.

In the event I add to this website, I may update this definition to include some elements contained in the update.

Website content &copy; 2024 Scott Lee Chua, all rights reserved.
