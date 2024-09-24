import marko
from marko.md_renderer import MarkdownRenderer
from marko.block import Paragraph, Heading, List, ListItem
from marko.inline import RawText
import cleantext
import nltk
import ssl


# this is a fix for this problem:
# https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# even while using the wrap around package cleantext is still necessary to download manually the packages
nltk.download("punkt_tab")
nltk.download("stopwords")


# recursively traverse the tree and only edit the text is some elements, the code blocks are excluded this way
# docs: https://marko-py.readthedocs.io/en/latest/api.html#marko.block.ListItem
def recursive_clean(element):
    if (isinstance(element, Paragraph) or
        isinstance(element, Heading) or
        isinstance(element, List) or
        isinstance(element, ListItem)
    ):
        for elem in element.children:
            recursive_clean(elem)
    elif isinstance(element, RawText):
        element.children = cleantext.clean(text=element.children, stemming=True, stopwords=True, stp_lang="english",
                                           extra_spaces=False)  # TODO should the extra spaces be removed????


def clean_string(text: str) -> str:
    try:
        # create a tree of md elements from text
        md_tree = marko.parse(text)
        for elem in md_tree.children:
            recursive_clean(elem)

        md_renderer = MarkdownRenderer()  # turn the tree back to string
        edited_text: str = md_renderer.render(md_tree)
        return edited_text

    except Exception as e:
        print(f"Error while parsing text: {text}")
        print(e)
        return text


# this was just for testing and playing around
if __name__ == '__main__':

    test1: str = """upgrade to rc1 dnx/runtime programs programmer

```bash
git clone https://github.com/natemcmaster/test-vscode-strong-name
cd test-vscode-strong-name
dnu restore programmer
code .
```

pick the Test project.json

result => ""Internal Class InternalClass is not accessible..."" error.

Works on OSX
    """

    # res = marko.parse(test1)

    test2: str = """Our linux build machine does not include the csharp-o/**bin** folder.
1. Running `scripts/npm.sh install` -> csharp-o/**bin** folder nicely gets created on my linux machine. programmers
2. Running `gulp vscode-linux-x64` also nicely creates the csharp-o/**bin** folder on my linux machine.

Something is strange on our build machine
    """

    res1 = clean_string(test1)

    res2 = clean_string(test2)

    pass
