class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.text = ""
        self.attributes = {}
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

    def __iadd__(self, other):
        if not self.is_single:
            self.children.append(other)
        else:
            pass
            # тогда надо добавлять элементы на том же уровне или игнорировать их
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self
        # if self.toplevel:
        #     print("<{}>".format(self.tag))
        #     for child in self.children:
        #         print(child)
        #     print("</{}>".format(self.tag))

    def __str__(self):
        attrs = ""
        for attribute, value in self.attributes.items():
            attrs += str(' {}="{}"'.format(attribute, value))

        if self.children:
            opening = "<{tag}{attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "{}".format(self.text)
            for child in self.children:
                internal += str(child)
            ending = "</{}>".format(self.tag)
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag}{attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag}{attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                    )


class HTML:
    def __init__(self, output):
        self.output = output
        self.children = []

    def __str__(self):
        if self.output is None:
            # print
            pass

    def __iadd__(self, other):
        self.children.append(other)


class TopLevelTag:
    def __init__(self, tag, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

    def __iadd__(self, other):
        self.children.append(other)



if __name__ == "__main__":

    with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
        # div.text = "ddd"
        with Tag("p") as p:
            p.text = "dfsfsd"
            div += p

        with Tag("img", is_single=True, src="/icon.png") as img:
            div += img

        print(div)


    # with HTML(output=None) as doc:
    #     with TopLevelTag("head") as head:
    #         with Tag("title") as title:
    #             title.text = "hello"
    #             head += title
    #         doc += head

    #     with TopLevelTag("body") as body:
    #         with Tag("h1", klass=("main-text",)) as h1:
    #             h1.text = "Test"
    #             body += h1

    #         with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
    #             with Tag("p") as paragraph:
    #                 paragraph.text = "another test"
    #                 div += paragraph

    #             with Tag("img", is_single=True, src="/icon.png") as img:
    #                 div += img

    #             body += div

    #         doc += body
