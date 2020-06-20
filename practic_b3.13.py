
class HTML:
    def __init__(self, output):
        self.tag = "html"
        self.output = output
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.children:
            opening = "<{tag}>\n".format(tag=self.tag)
            internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</{tag}>".format(tag=self.tag)
            result = opening + internal + ending
        else:
            result = "<{tag}></{tag}>".format(tag=self.tag)

        if self.output is None:
            print(result)
        else:
            with open(self.output, "w", encoding="UTF-8") as f:
                print(result, file=f)

    def __iadd__(self, other):
        self.children.append(other)
        return self


class TopLevelTag(HTML):
    def __init__(self, tag, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.children = []
        self.indent = 0

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

    def __exit__(self, type, value, traceback):
        return self

    def __str__(self):
        attrs = ""
        for attribute, value in self.attributes.items():
            attrs += str(' {}="{}"'.format(attribute, value))

        if self.children:
            opening = "<{tag}{attrs}>\n".format(tag=self.tag, attrs=attrs)
            internal = "{}".format(self.text)
            for child in self.children:
                child.indent = self.indent + 1
                internal += str(child)
            ending = "</{}>\n".format(self.tag)
            return opening + internal + ending
        else:
            return "<{tag}{attrs}>{text}</{tag}>\n".format(
                tag=self.tag, attrs=attrs, text=self.text
            )


class Tag(TopLevelTag):
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.text = ""
        self.attributes = {}
        self.children = []
        self.indent = 0

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

    def __iadd__(self, other):
        if not self.is_single:
            self.children.append(other)
        return self

    def __str__(self):
        whitespaces = (self.indent * 2) * " "
        attrs = ""
        for attribute, value in self.attributes.items():
            attrs += str(' {}="{}"'.format(attribute, value))

        if self.children:
            opening = "{indent}<{tag}{attrs}>".format(indent=whitespaces, tag=self.tag, attrs=attrs)
            internal = "{text}\n".format(text=self.text)
            for child in self.children:
                child.indent = self.indent + 1
                internal += str(child)
            ending = "{indent}</{tag}>\n".format(indent=whitespaces, tag=self.tag)
            return opening + internal + ending
        else:
            if self.is_single:
                return "{indent}<{tag}{attrs}/>\n".format(indent=whitespaces, tag=self.tag, attrs=attrs)
            else:
                return "{indent}<{tag}{attrs}>{text}</{tag}>\n".format(
                    indent=whitespaces, tag=self.tag, attrs=attrs, text=self.text
                )


if __name__ == "__main__":

    # Если output=None, то вывод на экран, иначе в файл, который указан.
    with HTML(output=None) as doc:
    # with HTML(output="doc.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body
