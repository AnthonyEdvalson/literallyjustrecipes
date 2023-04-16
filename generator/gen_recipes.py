import re
from typing import Union

import gpt

STYLE_PROMPT = """I am doing some brainstorming for a creative writing project.
Name an eccentric work of fiction, and fill out the following details:
1. Tone: how should the reader feel
2. Theme: what ideas does the creative work explore
3. Style: what kind of writing should be used to accomplish it, list 2-3 authors it is similar to
4. Genre: what is the genre of the work
5. Humor: how should humor be included in the piece
6. Setting: where does it take place
Answer each question with 1-2 sentences of detail. Provide no other output."""

ARC_PROMPT = """I'm working on a creative writing piece with the style:
{}

Create the outline for a short story with a beginning, middle and end based on the given style.
Focus on the protagonist, their character, motivations, and goals
Each part should be 1-2 sentences. Keep sentences concise and to the point.
Give all characters names except the protagonist who is named "Amelia Ivarson"
The story MUST begin with the protagonist making {}.
Output a numbered list item for the beginning, middle, and end. Output nothing else.
"""

BEAT_PROMPT = """Can you outline a short story with {} story beats based on that outline? 
Each beat should be 1-2 sentences. Keep sentences concise and to the point.
Focus on the protagonist, their character, motivations, and goals
Do not have the protagonist awaken in a strange room, or have amnesia.
Give all characters names except the protagonist who is named "Amelia Ivarson"
The first and last items in the list must ONLY involve the protagonist making {}
Output in a list format.
"""

INITIAL_PROMPT = """Write the preamble for an online recipe about {} that focuses on the first time you
prepared, consumed, or encountered the dish. 
Briefly and vaguely allude to:
{} 
But keep everything in the format of an online recipe. Include preparation details, ingredients, and quantities woven into the narrative.
Write 6 paragraphs"""

CONTINUE_PROMPT = """I'm working on a creative writing piece with the style:
{}

STORY BEATS:
{}

The last one is the most important.

CURRENT STORY:
{}

INSTRUCTIONS:
Please continue the story to fulfill story beat #{}
Use 6-12 paragraphs to work towards story beat #{}
Avoid narrative discontinuities or sudden changes in topic or jumps in time.
You are writing this as if you were Amelia Ivarson, describing the story as her personal anecdote.
Your additions should follow seamlessly from the story provided.
Use the word {} whenever appropriate."""

END_PROMPT = """Conclude the following story and add a seamless transition into a recipe for {}.

{}
"""

# Larger context sends more of the story for continuation. Gives it long-term consistency, but is more expensive
CTX_SIZE = 3000


def generate(food: str, blocks: int) -> str:
    style = ask(STYLE_PROMPT, 0.9)
    style = style.strip()

    style = re.findall(r"[0-9]+\. .*", style)
    if len(style) != 6:
        raise Exception("Did not create a valid style")
    style.append("7. Recurring Motif: {}".format(food))
    style = "\n".join(style)

    thread = [ARC_PROMPT.format(style, food)]
    arc = ask(thread, 0.2)
    thread.append(arc)
    thread.append(BEAT_PROMPT.format((blocks + 3) // 2, food))
    super_beats = ask(thread, 0.4)
    thread.append(super_beats)
    thread.append(BEAT_PROMPT.format(blocks, food))
    beats = ask(thread, 0.6)

    beats = re.findall(r"[0-9]+\. .*", beats)
    if len(beats) != blocks:
        raise Exception("Did not create valid beats")

    story = ask(INITIAL_PROMPT.format(food, beats[0][3:].replace("protagonist", "author").replace("Protagonist", "Author").replace("Amelia Ivarson", "author").replace("Amelia", "author")))
    story = trim_conclusion(story)
    for i in range(blocks)[1:]:
        story += ask(CONTINUE_PROMPT.format(style, "\n".join(beats[:i + 1]), story[-CTX_SIZE:], i + 1, i + 1, food))
        story = trim_conclusion(story)
    story += ask(END_PROMPT.format(food, story[-CTX_SIZE:]))

    print("Style")
    print(style)
    print()
    print("Outline")
    print("\n".join(beats))
    print()
    print("Story")
    print(story)

    return story


def ask(prompt: Union[str, list[str]], temperature=0.75) -> str:
    if type(prompt) is list:
        return gpt.chat(prompt, temperature)
    else:
        return gpt.chat([prompt], temperature)


def trim_conclusion(response: str) -> str:
    return "\n\n".join(response.split("\n\n")[:-1]) + "\n\n"


def main():
    food = input("Name a food: ")
    print("Creating a story...")
    story = generate(food, 12)
    print("Story finished!")
    with open("recipes/" + food + ".txt", "w+") as f:
        f.write(story)


if __name__ == '__main__':
    main()

