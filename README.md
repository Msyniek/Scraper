# Web Novel Scraper

This script automates the process of extracting text content from web novel sites and compiles the extracted chapters into a PDF file with proper formatting and custom fonts (supporting CJK characters).

## Features

- **Automated Chapter Navigation**: Automatically follows "下一章" (Next Chapter) links to scrape multi-chapter novels.
- **Content Extraction**: Handles two common HTML structures for Chinese web novels:
  - `<div id="txtcontent0">` (for twkan)
  - `<div class="txtnav">` (for 69shuba)
- **Cloudflare/JS Challenge Handling**: Uses `undetected_chromedriver` to bypass web protection mechanisms.
- **PDF Generation**: Outputs a formatted PDF using a custom CJK font for full Chinese character support.
- **Manual Line Wrapping**: Ensures text fits page width and paginates content.

## Requirements

Install dependencies with pip:

```
pip install requests beautifulsoup4 undetected-chromedriver reportlab
```

> **Note:** If you encounter issues, check the [official repo](https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues) for troubleshooting and updates.

## How It Works

1. **Initialization:**
   - Prompts user for starting URL, output PDF name, extraction method, and delay.
   - Sets up PDF canvas and registers the CJK font.

2. **Scraping Loop:**
   - Opens the chapter URL in a stealth browser.
   - Extracts narrative text based on chosen method.
   - Writes text to PDF, handling line wrapping and pagination.
   - Finds and follows the "下一章" link to the next chapter.
   - Repeats until no next chapter is found.

3. **Cleanup:**
   - Saves the PDF and quits the browser.
   - Prints success message and troubleshooting hints for known warnings.

## Troubleshooting

- **Font Issues:** Ensure the font file exists in `fonts\NotoSerifCJKsc-VF.ttf` and is readable.
- **Undetected Chromedriver Errors:** Ignorable if PDF is generated successfully. For details, see [issue #955](https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/955).
- **Cloudflare Blocks:** Increase the initial delay if necessary, or check browser compatibility.

## Example Usage

```text
Enter the start URL: https://www.69shuba.com/txt/84513/example
Enter the PDF file name (default: example.pdf): my_novel.pdf
Using font file: your_path\fonts\NotoSerifCJKsc-VF.ttf
Font exists: True
Is the font readable? True
Choose extraction method:
1. Extract from <div id='txtcontent0'> (twkan)
2. Extract from <div class='txtnav'> (69)
Enter 1 or 2: 2
Enter the time to delay between requests (Cloudflare)(default: 2): 3
Content saved to your_path\Scraper\my_novel.pdf
```

## License

MIT License

## Credits

- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- [Noto CJK Fonts](https://github.com/notofonts/noto-cjk)
- [reportlab](https://pypi.org/project/reportlab/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)
