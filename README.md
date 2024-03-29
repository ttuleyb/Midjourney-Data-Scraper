# Midjourney-Data-Scraper
This tool is the full package for fine tuning a language model to generate MJ prompts for you.

## What tools does this repo include?

- Archiver
- Benchmark
- File merging script
- Data cleaner/filtering tools
- Data counter (JSON)
- Data counter (Text)
- Data counter (MongoDB)
- Data scraping tools
- Json merger
- MongoDB index creator
- MongoDB append entries

## How does this cross over with PromptGods?
PromptGods is a prompting tool I'm working on. I want it to be the be-all end-all prompting tool.
Check out the [PromptGods repo](https://github.com/ttuleyb/PromptGods) for updated versions of some of the tools like data cleansing.

## Tools you should refrain from using
Any tool I have labelled with (rate limit) should be used carefully or you risk taking down the midjourney gallery.

### Archiver
This tool checks all new files under the jsons folder then adds them under a folder named after the current date in the archive root directory

### Benchmark (rate limit)
Outdated tool that checks how long it takes to send requests.

### File merging script
Pretty self explanatory, takes in a bunch of text files then merges them into one

### Data cleaner
Takes in your data and then cleans links aswell as performs other functions to filter the data. It then appends all the data in a TSV file in the format usable to fine-tune OpenAI GPT models.

### Data counter
Counts the number of unique prompts in a given file

### Database counter
Counts the number of entries in MongoDB

### Json Reader (and merger)
Reads all json files in a given directory then merges all of the prmpts in a single txt file

### Data scraping tools

#### Legacy scrapers (rate limit)
These work by requesting all pages for listed sorting methods. They go page by page (in multiple threads) and download the midjourney gallery's frontpage.

#### Modern scrapers
This script works by using the voting algorithm to download this weeks most highly rated images all in a single request.
I heavily recommend using this script over the legacy scrapers as it is faster and puts a lot less load on the midjourney database as it seems like their voting function is much more optimized compared to their frontpage.
The only downside is that you only get the highest rated data compared to legacy which would give you a lot more data to work with.

### Mongo Indexer
Creates basic indexes for MongoDB to reduce access time when requesting data

### Mongo Appending tool
mongo_db.py
This tool appends all files under a given folder to MongoDB.
