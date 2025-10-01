# Static website generator

A Python-based static site generator that converts Markdown files into a fully-functional static website. This project provides a complete solution for building static websites from Markdown content with automatic HTML generation, CSS styling, and asset management.

## What It Does

This static site generator:
- Converts Markdown files into HTML pages using a customizable template
- Processes inline Markdown syntax (bold, italic, code, links, images)
- Handles various Markdown block types (headings, paragraphs, lists, code blocks, quotes)
- Automatically copies static assets (CSS, images) to the output directory
- Generates a complete website structure ready for deployment
- Supports recursive directory processing for organized content

## Features

- **Markdown to HTML Conversion**: Full support for standard Markdown syntax
- **Flexible Content Organization**: Organize your content in nested directories
- **Static Asset Management**: Automatic copying of CSS and images
- **Customizable Templates**: Use HTML templates with placeholder replacement
- **URL Path Configuration**: Support for custom base paths for deployment
- **Recursive Generation**: Automatically processes all Markdown files in subdirectories

## Prerequisites

- Python 3.13 or higher (tested with Python 3.12+)
- No external dependencies required (uses only Python standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ManoloEsS/my_static_website.git
cd my_static_website
```

2. The project uses only Python standard library, so no additional package installation is needed.

## Usage

### Building the Website

To generate the static website, run:

```bash
bash build.sh
```

This command:
1. Deletes the existing `docs` directory (if present)
2. Copies all files from `static/` to `docs/`
3. Converts all Markdown files from `content/` to HTML in `docs/`

For custom base paths (useful for GitHub Pages or subdirectory hosting):
```bash
python3 -m src.main "/your-base-path/"
```

### Running the Development Server

To preview your site locally:

```bash
bash main.sh
```

This will:
1. Build the website
2. Start a local HTTP server on port 8888
3. Open your browser to http://localhost:8888

### Running Tests

To run the test suite:

```bash
bash test.sh
```

Or directly:
```bash
python3 -m unittest discover -s tests
```

## Project Structure

```
my_static_website/
├── src/                      # Source code
│   ├── main.py              # Main entry point
│   ├── generate_content.py  # HTML generation from Markdown
│   ├── markdown_blocks.py   # Markdown block parsing
│   ├── inline_markdown.py   # Inline Markdown processing
│   ├── htmlnode.py          # HTML node representation
│   ├── textnode.py          # Text node representation
│   └── copystatic.py        # Static file copying utilities
├── content/                  # Markdown source files
│   ├── index.md             # Homepage content
│   ├── blog/                # Blog posts
│   └── contact/             # Contact page
├── static/                   # Static assets (CSS, images)
│   ├── index.css            # Stylesheet
│   └── images/              # Image files
├── docs/                     # Generated output (created by build)
├── tests/                    # Unit tests
├── template.html             # HTML template for pages
├── build.sh                  # Build script
├── test.sh                   # Test script
└── main.sh                   # Build and serve script
```

## How It Works

1. **Content Preparation**: Write your content in Markdown files in the `content/` directory
2. **Template**: The `template.html` file defines the structure with `{{ Title }}` and `{{ Content }}` placeholders
3. **Build Process**:
   - Static assets are copied from `static/` to `docs/`
   - Markdown files are parsed and converted to HTML
   - HTML is injected into the template
   - Final HTML files are written to `docs/`
4. **Output**: The `docs/` directory contains your complete static website

## Adding Content

1. Create a new Markdown file in the `content/` directory (e.g., `content/blog/my-post/index.md`)
2. Write your content using standard Markdown syntax
3. Ensure each Markdown file has an H1 header (e.g., `# My Post Title`)
4. Run the build script to generate the HTML

### Supported Markdown Syntax

- Headers: `# H1`, `## H2`, etc.
- Bold: `**bold text**`
- Italic: `*italic text*`
- Code: `` `inline code` ``
- Code blocks: ` ``` code block ``` `
- Links: `[link text](url)`
- Images: `![alt text](image-url)`
- Unordered lists: `- item`
- Ordered lists: `1. item`
- Quotes: `> quote text`

## Customization

### Modifying the Template

Edit `template.html` to change the structure and styling of your pages. The template uses two placeholders:
- `{{ Title }}`: Replaced with the H1 heading from the Markdown
- `{{ Content }}`: Replaced with the converted HTML content

### Styling

Modify `static/index.css` to customize the appearance of your website.

## Deployment

The generated `docs/` directory is ready for deployment to:
- GitHub Pages (configure your repository to serve from the `docs` folder)
- Any static hosting service (Netlify, Vercel, etc.)
- Traditional web servers

## License

This project was created as part of the [Build a Static Site Generator](https://www.boot.dev/courses/build-static-site-generator-python) course on [Boot.dev](https://www.boot.dev).

## Contributing

Feel free to submit issues and enhancement requests!
