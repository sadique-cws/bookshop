import random
import string
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings

from ecom.models import Author, Genere, Book


SAMPLE_GENRES = [
    "Science Fiction",
    "Fantasy",
    "Mystery",
    "Romance",
    "Horror",
    "History",
    "Biography",
    "Self Help",
    "Poetry",
    "Philosophy",
]


SAMPLE_TITLES = [
    "Shadows of Time",
    "The Last Harbor",
    "Whispers of the Old House",
    "The Glass Orchard",
    "Echoes of Tomorrow",
    "Paper Moons",
    "The Rusted Key",
    "Winds of Winter",
    "City of Lanterns",
    "Beneath the Ocean",
]


def random_paragraph(sentences=3):
    words = (
        "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
    ).split()
    out = []
    for _ in range(sentences):
        length = random.randint(6, 18)
        out.append(" ".join(random.choices(words, k=length)).capitalize() + ".")
    return "\n\n".join(out)


def random_isbn():
    return "".join(random.choices(string.digits, k=13))


class Command(BaseCommand):
    help = "Seed the database with sample genres, authors and books (with images)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--books",
            type=int,
            default=40,
            help="Number of books to create (default: 40)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing Book/Author/Genere objects before seeding",
        )

    def handle(self, *args, **options):
        num_books = options["books"]
        clear = options["clear"]

        # determine image source directory
        base_dir = getattr(settings, "BASE_DIR", Path(__file__).resolve().parent.parent.parent.parent)
        candidates = [
            Path(base_dir) / "books" / "cover",
            Path(base_dir) / "media" / "books" / "cover",
        ]
        image_files = []
        for c in candidates:
            if c.exists() and c.is_dir():
                image_files = [p for p in c.iterdir() if p.is_file()]
                if image_files:
                    break

        if not image_files:
            self.stderr.write(self.style.ERROR(
                f"No cover images found in any of: {candidates}. Please add images to one of those folders before running the seeder."
            ))
            return

        if clear:
            Book.objects.all().delete()
            Author.objects.all().delete()
            Genere.objects.all().delete()
            self.stdout.write("Cleared existing Book, Author and Genere entries.")

        # create genres
        genres = []
        for i, g in enumerate(SAMPLE_GENRES):
            slug = slugify(g)
            obj, created = Genere.objects.get_or_create(title=g, slug=slug)
            genres.append(obj)

        # create some extra generic genres if needed
        while len(genres) < max(6, num_books // 6):
            title = f"Genre {len(genres) + 1}"
            slug = slugify(title)
            obj, _ = Genere.objects.get_or_create(title=title, slug=slug)
            genres.append(obj)

        # create authors
        authors = []
        first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan",
        ]
        last_names = [
            "Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas", "Jackson", "White",
            "Harris", "Martin",
        ]

        num_authors = max(8, num_books // 3)
        for i in range(num_authors):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            slug = slugify(name)
            email = f"{slug.replace('-', '')}@example.com"
            contact = "".join(random.choices(string.digits, k=10))
            obj, _ = Author.objects.get_or_create(name=name, slug=slug, defaults={"email": email, "contact": contact})
            authors.append(obj)

        # create books
        created_books = 0
        for i in range(num_books):
            title = f"{random.choice(SAMPLE_TITLES)} {i+1}"
            slug = slugify(title)
            price = round(random.uniform(5.0, 120.0), 2)
            discount_price = price - round(random.uniform(0, price * 0.4), 2) if random.random() < 0.4 else None
            description = random_paragraph(sentences=random.randint(2, 5))
            no_of_pages = random.randint(80, 900)
            author = random.choice(authors)
            genere = random.choice(genres)
            isbn = random_isbn()

            book = Book(
                title=title,
                slug=slug,
                price=price,
                discount_price=discount_price,
                description=description,
                no_of_pages=no_of_pages,
                author=author,
                genere=genere,
                edition="Latest Edition",
                isbn=isbn,
            )

            # attach image
            img_path = random.choice(image_files)
            try:
                with open(img_path, "rb") as fh:
                    django_file = File(fh)
                    # safe file name
                    suffix = img_path.suffix
                    name = f"{slug}-{i}{suffix}"
                    book.cover_image.save(name, django_file, save=False)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to attach image {img_path}: {e}"))
                continue

            book.save()
            created_books += 1
            if created_books % 5 == 0:
                self.stdout.write(f"Created {created_books} books so far...")

        self.stdout.write(self.style.SUCCESS(f"Seeding complete: created {created_books} books, {len(authors)} authors, {len(genres)} genres."))
