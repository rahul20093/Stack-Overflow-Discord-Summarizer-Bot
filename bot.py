import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open('config.json', 'r') as f:
    config = json.load(f)
    
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

def scrape_so_question(question_link: str):
    """
    Scrapes a Stack Overflow question page for the title, body, and accepted answer.
    """
    try:
        response = requests.get(question_link)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        question_title = soup.find('a', class_='question-hyperlink').text.strip()

        question_body_element = soup.find('div', class_='s-prose js-post-body')
        question_body = question_body_element.text.strip() if question_body_element else "Could not find question body."
        question_body = question_body[:500] + '...' if len(question_body) > 500 else question_body

        answer_body = "No accepted or positively voted answer found."
        accepted_answer = soup.find('div', class_='answer accepted-answer')
        if not accepted_answer:
            answers = soup.find_all('div', class_='answer', attrs={'data-score': True})
            for answer in answers:
                if int(answer['data-score']) > 0:
                    accepted_answer = answer
                    break

        if accepted_answer:
            answer_body_element = accepted_answer.find('div', class_='s-prose js-post-body')
            if answer_body_element:
                answer_body = answer_body_element.text.strip()
                answer_body = answer_body[:500] + '...' if len(answer_body) > 500 else answer_body

        return {
            "title": question_title,
            "body": question_body,
            "answer": answer_body
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching the Stack Overflow page: {e}"}
    except Exception as e:
        return {"error": f"An error occurred during scraping: {e}"}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def so(ctx, *, question_link: str):
    
    scraped_data = scrape_so_question(question_link)

    if "error" in scraped_data:
        await ctx.send(scraped_data["error"])
        return

    embed = discord.Embed(title=scraped_data["title"], url=question_link, description=scraped_data["body"])
    embed.add_field(name="Answer", value=scraped_data["answer"], inline=False)
    embed.set_footer(text="Fetched from Stack Overflow")

    await ctx.send(embed=embed)

bot.run(TOKEN)