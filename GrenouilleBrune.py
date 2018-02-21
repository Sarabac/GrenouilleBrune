from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import NoEscape
import os


def dessiner(doc, chemin):
    for photo in os.listdir(chemin):
        with doc.create(Section('Showing subfigures')):
            image_filename = os.path.join(chemin, photo)
            with doc.create(Figure(width=NoEscape(r'\linewidth'))) as frog:
                frog.add_image(image_filename, width=NoEscape(r'\linewidth'))


if __name__ == '__main__':
    # Basic document
    doc = Document("GrenouilleBrune")

    doc.preamble.append(Command('title', 'Awesome Title'))
    doc.preamble.append(Command('author', 'Lucas Boutarfa'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    doc.append(Command("section", NoEscape(r"Une section")))
    doc.append('du Texte')

    dessiner(doc, "test")
    doc.create(Section("une autre section"))
    doc.append("plus de texte")
    doc.generate_pdf(clean_tex=False)
    doc.generate_tex()
    #print(doc.dumps())
