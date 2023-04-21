import random
import re
from typing import Union

import gpt
from generator.Prompt import Prompt, Section

MAKE_STYLE = Section("INSTRUCTIONS", """I am doing some brainstorming for a creative writing project.
Fill out the following details for the book {base_book}.
1. Tone: how should the reader feel
2. Theme: what ideas does the creative work explore
3. Style: Name an author that write in a style similar to the book
4. Genre: what is the genre of the work
5. Humor: how should humor be included in the piece
6. Setting: what kind of environment the events take place. Don't give specific names

In your answers, don't reference the name or author of the original work.
Answer each question with 1-2 sentences. Provide no other output.""")

MAKE_OUTLINE = Section("INSTRUCTIONS", """Create the outline for a short story with a beginning, middle and end based on the given style.
Focus on the protagonist, their character, motivations, and goals
Each part should be at least a paragraph. Keep sentences concise and to the point.
Name all characters, the protagonist is named "Amelia Iverson"
The story MUST begin with the protagonist making {food}.""")

MAKE_CHAPTERS = Section("INSTRUCTIONS", """Expand the outline to a summary of exactly {chapter_count} chapters. 
Keep sentences concise and to the point.
Mention places that need to be described, and people to introduce.
Name all characters, the protagonist is named "Amelia Iverson"
The first and last items in the list must ONLY involve the protagonist making {food}
Include chapters for travelling between locations.
Include chapters for character building and exploration.
Only output a list of chapters with at least a paragraph each. DO NOT output anything other than the list.""")

WRITE_CHAPTER = Section("INSTRUCTIONS", """"Write chapter {chapter_num} of the story, it should be short, about 8 paragraphs long.
Do not copy any exact phrasing from the outline. All prose should be original
Avoid abrupt changes in time, place, or topic, explain all transitions and describe all changes.
Include {food} whenever appropriate.
Describe Amelia's thoughts and sensory details whenever possible, but avoid clichés and generic phrasing. Sensory details should be specific to the scene and the story.
The story is written by Amelia Iverson, describing the story as her personal anecdote in first person.
Output the text of the chapter and nothing else.""")


END_PROMPT = """Conclude the following story and add a seamless transition into a recipe for {}.

{}"""

RECIPE_PROMPT = """Create a recipe for {}. Include:
1. A list of ingredients and their amounts
2. A list of instructions
3. A message at the end telling the reader to eat and enjoy the food they have prepared."""

DO_MERGE = Section("INSTRUCTIONS", """Apply those changes to the content. 
Combine as many details as possible from your notes with original content. 
Do not remove any information in the content.
Output a new version of the content, and nothing else. DO NOT explain your edits or list any changes made.""")

DO_EXPAND = Section("INSTRUCTIONS", """Add new details to the content including:
- Sensations (sights, smells, touch, etc.)
- Thoughts of the protagonist
- Worldbuilding information
- Symbolism
- Dialogue between characters (if appropriate)

Adhere to standard writing principles like show, don't tell.

Don't add new events, only new observations.
Don't explain your changes, just show the revised content""")


DO_REVISE = Section("INSTRUCTIONS", """What 3 simple changes would most improve the content and make it suitable for a published novel? Examples:
- Add sensory details
- Expand on dialogue
- Add symbolism or deeper meanings
- Replace an unusual phrase or idea that doesn't fit.
Give concise answers""")


def revise(attrs: dict[str, str], sections: list[Section], content_str: str, log: list[tuple[str, str]]) -> str:
    content = Section("CONTENT", content_str)
    revise_prompt = Prompt(*sections, content, DO_REVISE).format(attrs)
    changes = ask(revise_prompt, 0.4, log)

    new_content = merge(attrs, content_str, changes, log)

    return new_content.strip()


def elaborate(attrs: dict[str, str], sections: list[Section], content_str: str, log: list[tuple[str, str]]) -> str:
    content = Section("CONTENT", content_str)

    instruction = Section("INSTRUCTIONS", "List up to 5 things that stand out as being vague or unanswered.")
    question_prompt = Prompt(*sections, content, instruction).format(attrs)
    problems = Section("PROBLEMS", ask(question_prompt, 0.3, log))

    instruction = Section("INSTRUCTIONS", "List answers to those problems. Make sure the answers are consistent with "
                                         "the story's style. All answers should be concrete, and not left vague. Do not dismiss any questions, the listed problems are valid and need to be addressed.")
    answer_prompt = Prompt(*sections, content, problems, instruction).format(attrs)
    changes = ask(answer_prompt, 0.5, log)

    new_content = merge(attrs, content_str, changes, log)

    return new_content.strip()


def expand(attrs: dict[str, str], sections: list[Section], content: str, log: list[tuple[str, str]]) -> str:
    expand_prompt = Prompt(*sections, Section("CONTENT TO EDIT", content), DO_EXPAND).format(attrs)
    content = ask(expand_prompt, 0.5, log)
    return content.strip()


def merge(attrs: dict[str, str], content: str, changes: str, log: list[tuple[str, str]]) -> str:
    content_section = Section("CONTENT TO CHANGE", content)
    change_section = Section("CHANGES", changes)
    mix_prompt = Prompt(content_section, change_section, DO_MERGE).format(attrs)
    return ask(mix_prompt, 0.2, log)


# Larger context sends more of the story for continuation. Gives it long-term consistency, but is more expensive
CTX_SIZE = 4000

with open("generator/booklist.txt") as f:
    all_books = f.read().split("\n")


def generate_style(attrs: dict[str, str], log: list[tuple[str, str]]):
    base_book = random.choice(all_books)
    prompt = Prompt(MAKE_STYLE).format(attrs, base_book=base_book)
    style = ask(prompt, 0.7, log)

    style = list_response(style, r"^(style|content|response)$", "{}. {}")
    assert len(style) == 6
    style.append("7. Recurring Motif: {food}".format(**attrs))
    style.append("8. Topics: Avoid topics like slavery, gender, race, and graphic violence.")
    style.append("9. Rating: PG-13")
    style.append("10. Protagonist Name: Amelia Iverson")
    style.append("11. Perspective: First Person")
    style = "\n".join(style)

    return style


def generate_chapters(attrs: dict[str, str], style: Section, log: list[tuple[str, str]]) -> list[str]:
    outline_prompt = Prompt(style, MAKE_OUTLINE).format(attrs)
    outline = ask(outline_prompt, 0.8, log)

    outline = elaborate(attrs, [style], outline, log)

    to_chapters_prompt = Prompt(style, Section("OUTLINE", outline), MAKE_CHAPTERS).format(attrs)
    chapters = ask(to_chapters_prompt, 0.6, log)

    chapters = elaborate(attrs, [style], chapters, log)
    chapters = revise(attrs, [style], chapters, log)

    return list_response(chapters, r"^(content( to edit)?|chapters)$", "Chapter {}: {}")


def generate_chapter(attrs: dict[str, str], style: Section, outline: Section, chapter_summaries: list[str], chapter_index: int, log: list[tuple[str, str]]):
    chapter_num = chapter_index + 1
    chapter_outline = chapter_summaries[chapter_index]
    chapter_outline = Section("CHAPTER {} OUTLINE".format(chapter_num), chapter_outline)
    if chapter_index > 0:
        previous_chapter = chapter_summaries[chapter_index - 1]
        previous_chapter = Section("PREVIOUS CHAPTER".format(chapter_num - 1), previous_chapter[-2500:])
        write_prompt = Prompt(style, outline, previous_chapter, WRITE_CHAPTER, chapter_outline).format(attrs, chapter_num=chapter_num)
    else:
        write_prompt = Prompt(style, outline, WRITE_CHAPTER, chapter_outline).format(attrs, chapter_num=chapter_num)

    content = ask(write_prompt, 0.5, log)

    content = elaborate(attrs, [style, outline, chapter_outline], content, log)
    content = expand(attrs, [style, outline, chapter_outline], content, log)
    #content = revise(attrs, [style, outline, chapter_outline], content, log)

    return content


def generate(food: str, blocks: int) -> tuple[str, list[tuple[str, str]]]:
    attrs: dict[str, str] = {"food": food, "chapter_count": blocks}
    while True:
        log: list[tuple[str, str]] = []
        style = Section("STYLE", generate_style(attrs, log))
        if not looks_good(style.content):
            continue

        chapter_summaries = generate_chapters(attrs, style, log)
        if not looks_good("\n".join(chapter_summaries)):
            continue
        outline = Section("OUTLINE", "\n\n".join(chapter_summaries))

        chapters = []
        for i in range(len(chapter_summaries)):
            chapter = generate_chapter(attrs, style, outline, chapter_summaries, i, log)
            chapters.append(chapter)

        story = "\n\n---\n\n".join(chapters)

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


def list_response(response: str, tag: str, item_format: str) -> list[str]:
    parts = re.split(r"(?m)^#+ (.*)]", response, re.IGNORECASE)
    section = None
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            if re.search(tag, parts[i].strip()) is not None:
                section = parts[i + 1]
                break
    else:
        section = response

    if section is None:
        raise Exception("Unable to locate {} in parts {}".format(tag, parts))

    parts = re.split(r"(?m)^(?:(?:[a-zA-Z0-9]+\.)|(?:[a-zA-Z0-9]+(?: [a-zA-Z0-9]+)?(?::| -)))", section)[1:]
    parts = list(filter(lambda s: len(s.strip()) > 0, parts))
    return [item_format.format(n + 1, text.strip()) for n, text in enumerate(parts)]


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

