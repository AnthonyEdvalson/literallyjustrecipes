class Section:
    def __init__(self, key: str, content: str):
        self.key = key
        self.content = content

    def format(self, attrs: dict[str, str], **kwargs):
        return "# {}\n{}".format(self.key, self.content.format(**attrs, **kwargs))

    def with_name(self, new_key: str) -> 'Section':
        return Section(new_key, self.content)


class Prompt:
    def __init__(self, *sections: Section):
        self.sections = sections

    def format(self, attrs: dict[str, str], **kwargs):
        return "\n\n".join([section.format(attrs, **kwargs) for section in self.sections])
