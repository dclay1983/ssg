from textnode import TextNode, TextType

tn = TextNode("This is some anchor text", TextType.LINK, "www.google.com/")
print(tn)
