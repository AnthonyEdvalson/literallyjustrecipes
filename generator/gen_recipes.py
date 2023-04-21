import random
import re
from typing import Union

import gpt

STYLE_PROMPT = """I am doing some brainstorming for a creative writing project.
Fill out the following details for the book {}.
1. Tone: how should the reader feel
2. Theme: what ideas does the creative work explore
3. Style: Name an author that write in a style similar to the book
4. Genre: what is the genre of the work
5. Humor: how should humor be included in the piece
6. Environment: what kind of environment the events take place. Don't give specific names

In your answers, don't reference the name or author of the original work.
Answer each question with 1-2 sentences. Provide no other output."""

OUTLINE_PROMPT = """I'm working on a creative writing piece with the style:
{}

Create the outline for a short story with a beginning, middle and end based on the given style.
Focus on the protagonist, their character, motivations, and goals
Each part should be at least a paragraph. Keep sentences concise and to the point.
Name all characters, the protagonist is named "Amelia Ivarson"
The story MUST begin with the protagonist making {}.
"""

CHAPTER_PROMPT = """Expand the outline to a summary of exactly {} chapters. 
Keep sentences concise and to the point.
Mention places that need to be described, and people to introduce.
Name all characters, the protagonist is named "Amelia Ivarson"
The first and last items in the list must ONLY involve the protagonist making {}
Include chapters for travelling between locations.
Include chapters for character building and exploration.
Only output a list of chapters with at leas a paragraph of notes for each. Do not output anything other than the list
"""

INITIAL_PROMPT = """Write the preamble for an online recipe about {} that focuses on the first time you
prepared, consumed, or encountered the dish. 
At the end, briefly and vaguely allude to:
{} 
But keep everything in the format of an online recipe. Include preparation details, ingredients, and quantities woven into the narrative.
Do not talk about anything other than making the recipe.
Write 4 paragraphs"""

CHAPTER_HEAD_PROMPT = """I'm working on a creative writing piece with the style:
{}

CHAPTER SUMMARIES:
{}

INSTRUCTIONS:
Please write chapter {} of the story, it should be short, about 6 paragraphs long.
Do not copy any exact phrasing from the document. All prose should be original
Avoid abrupt changes in time, place, or topic, explain all transitions and describe all changes.
Include {} whenever appropriate.
When going to a new place, describe details. Like how they get there, how long it took, and other sensory information.
Describe Amelia's thoughts and sensory details whenever possible, but avoid clichés or commonly used anecdotes. Sensory details should be specific to the scene and the story.
You are writing this as if you were Amelia Ivarson, describing the story as her personal anecdote.
Output the text of the chapter and nothing else."""

CHAPTER_CONTINUE_PROMPT = """Continue by writing chapter {} seamlessly from the previous chapter.

CONSTRAINTS:
- 6-10 paragraphs
- Do not copy any exact phrasing from the summary.
- All text should be written as if it were from a professional fiction novel.
- Avoid summaries and descriptions of conversations and events, add the dialogue between characters, and details to make the story come alive.
- Give specific details on as much as possible fill in gaps not covered in the summary.
- The story is written from Amelia's perspective, describing the story as a personal anecdote in the first person.
- Output the text of the chapter and nothing else.

CHAPTER SUMMARY:
{}"""

END_PROMPT = """Conclude the following story and add a seamless transition into a recipe for {}.

{}
"""

RECIPE_PROMPT = """Create a recipe for {}. Include:
1. A list of ingredients and their amounts
2. A list of instructions
3. A message at the end telling the reader to eat and enjoy the food they have prepared."""


def mix_prompt(noun: str) -> str:
    return """Apply those notes to the previous {0:}. 
Combine as many details as possible from your notes with original {0:}. 
Do not remove any information in the {0:}.
Output the {0:}, and nothing else. Do not explain your edits or list the changes made.""".format(noun)


def revise_loop(noun: str) -> list[str]:
    return [
        """What 4 things would most improve the {0:} and make it suitable for a published novel? Examples:
- Add more sensory details
- Add more characters / dialogue
- Add more drama
- Add symbolism or deeper meanings
- Replace an unusual phrase or idea that doesn't fit in or is inappropriate.
Give concise answers""".format(noun),
        mix_prompt(noun)
    ]


def explain_loop(noun: str) -> list[str]:
    return [
        "Name up to 4 things that stand out as being vague or unanswered.",
        "List answers to those problems. Make sure the answers are consistent with the story's style. All answers should be concrete, and not left vague.",
        mix_prompt(noun)
    ]


def expand_prompt(noun: str) -> str:
    return """Add new details including:
- Sensations (sights, smells, touch, etc.)
- Thoughts of the protagonist
- Worldbuilding information
- Symbolism
- Dialogue between characters (if appropriate)

Adhere to standard writing principles like show, don't tell.

Don't add new events, only new observations.
Don't explain your changes, just show the revised {}""".format(noun)


# Larger context sends more of the story for continuation. Gives it long-term consistency, but is more expensive
CTX_SIZE = 4000

with open("generator/booklist.txt") as f:
    all_books = f.read().split("\n")


def generate(food: str, blocks: int) -> tuple[str, list[tuple[str, str]]]:
    chapter_summaries = []
    while True:
        log: list[tuple[str, str]] = []
        book = random.choice(all_books)
        style = ask(STYLE_PROMPT.format(book), 0.7, log)
        style = list_response(style, "{}. {}")
        style.append("7. Recurring Motif: {}".format(food))
        style.append("8. Topics: Avoid topics like slavery, gender, race, and graphic violence.")
        style.append("9. Rating: PG-13")
        style = "\n".join(style)

        if not looks_good(style):
            continue

        outline_prompt = OUTLINE_PROMPT.format(style, food)
        outline_revisions = [
            explain_loop("outline"),
            [CHAPTER_PROMPT.format(blocks, food)],
            #revise_loop("outline"),
            #explain_loop("outline"),
            #revise_loop("outline"),
            [expand_prompt("outline")],
            explain_loop("outline"),
            revise_loop("outline"),
        ]
        chapter_summaries = make_and_revise([], outline_prompt, outline_revisions, 0.4, log)
        chapter_summaries = list_response(chapter_summaries, "Chapter {}: {}")
        if not looks_good("\n\n".join(chapter_summaries)):
            continue
        break

    sanitized_chapter_one = chapter_summaries[0][12:]\
        .replace("protagonist", "author")\
        .replace("Protagonist", "Author")\
        .replace("Amelia Ivarson", "author")\
        .replace("Amelia", "author")
    initial_prompt = INITIAL_PROMPT.format(food, sanitized_chapter_one)
    chapters = [trim_conclusion(ask(initial_prompt, 0.5, log))]

    for i in range(len(chapter_summaries))[1:]:
        thread = [
            CHAPTER_HEAD_PROMPT.format(style, "\n".join(chapter_summaries), i, food),
            chapters[i-1][-2500:]
        ]
        continue_prompt = CHAPTER_CONTINUE_PROMPT.format(i + 1, chapter_summaries[i])
        revision_prompts = [
            explain_loop("chapter"),
            [expand_prompt("chapter")],
            revise_loop("chapter"),
        ]

        chapter_final = make_and_revise(thread, continue_prompt, revision_prompts, 0.2, log)

        chapters.append(chapter_final.strip())

    story = "\n\n---\n\n".join(chapters)
    """
    sanitized_chapter_one = chapters[0][3:].replace("protagonist", "author").replace("Protagonist", "Author").replace("Amelia Ivarson", "author").replace("Amelia", "author")
    initial_prompt = INITIAL_PROMPT.format(food, sanitized_chapter_one)
    story = ask(initial_prompt, 0.5, log)
    story = trim_conclusion(story)
    for i in range(blocks)[1:]:
        block_prompt = CONTINUE_PROMPT.format(style, "\n".join(chapters[:i + 1]), story[-CTX_SIZE:], i + 1, i + 1, food)
        block = trim_conclusion(ask(block_prompt, 0.5, log))
        story += block"""

    end_prompt = END_PROMPT.format(food, story[-CTX_SIZE:])
    ending = ask(end_prompt, 0.4, log)
    chapters += ending

    print("Style")
    print(style)
    print()
    print("Outline")
    print("\n".join(chapter_summaries))
    print()
    print("Story")
    print(story)

    return story, log


def looks_good(thing: str):
    print()
    print(thing)
    return input("Look good?")[0].lower() == "y"


def prompt_chain(initial_thread: list[str],
                 prompts: list[str],
                 temperature: float,
                 log: list[tuple[str, str]]):
    thread = [*initial_thread]
    for edit_prompt in prompts:
        thread.append(edit_prompt)
        response = ask(thread, temperature, log)
        thread.append(response)
    return thread[-1]


def revise_chain(initial_thread: list[str],
                 initial_value: str,
                 prompt_set: list[list[str]],
                 temperature: float,
                 log: list[tuple[str, str]]):
    value = initial_value
    for prompts in prompt_set:
        if type(prompts) != list:
            raise TypeError("Prompts must be a list.")
        value = prompt_chain([*initial_thread, value], prompts, temperature, log)
    return value


def make_and_revise(initial_thread: list[str],
                    make_prompt: str,
                    prompt_set: list[list[str]],
                    temperature: float,
                    log: list[tuple[str, str]]):
    initial = prompt_chain(initial_thread, [make_prompt], temperature, log)
    return revise_chain([make_prompt], initial, prompt_set, temperature, log)


def list_response(response: str, tag_format: str) -> list[str]:
    numbers_and_text = re.split(r"(?m)^[^0-9\n]{,40}([0-9]+)[:.]", response)
    numbers = numbers_and_text[1::2]
    text = numbers_and_text[2::2]
    return [tag_format.format(n, text.strip()) for n, text in zip(numbers, text)]


def ask(prompt: Union[str, list[str]], temperature: float, log: list[tuple[str, str]]) -> str:
    if type(prompt) is list:
        log.extend([("user", p) for p in prompt])
        response = gpt.chat(prompt, temperature)
    else:
        log.append(("user", prompt))
        response = gpt.chat([prompt], temperature)
    log.append(("system", response))
    return response


def trim_conclusion(response: str) -> str:
    return "\n\n".join(response.split("\n\n")[:-1]) + "\n\n"


def main():
    food = input("Name a food: ")
    print("Creating a story...")
    story, logs = generate(food, 5)
    print("Story finished!")
    with open("recipes/" + food + "_log.txt", "w+") as f:
        f.write("\n".join(["{} > {}".format(u, t) for u, t in logs]))
    with open("recipes/" + food + ".txt", "w+") as f:
        f.write(story)


if __name__ == '__main__':
    main()

