#!/usr/bin/env python3
import re
import json
from html.parser import HTMLParser
from urllib.parse import unquote

class ProductExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = []
        self.current_product = {}
        self.in_figure = False
        self.in_link = False
        self.in_caption = False
        self.current_link = ""
        self.current_caption = ""
        self.current_image = ""
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'figure':
            self.in_figure = True
            self.current_product = {}
            
        elif tag == 'a' and self.in_figure:
            self.in_link = True
            if 'href' in attrs_dict:
                self.current_link = attrs_dict['href']
                
        elif tag == 'img' and self.in_figure:
            # Try to get image from data-src or src
            if 'data-src' in attrs_dict:
                img_url = attrs_dict['data-src']
            elif 'src' in attrs_dict:
                img_url = attrs_dict['src']
            else:
                img_url = ""
            
            # Extract filename from URL
            if img_url:
                # Decode URL encoding
                img_url = unquote(img_url)
                # Extract filename (last part after /)
                filename = img_url.split('/')[-1]
                # Remove query parameters
                filename = filename.split('?')[0]
                # Handle URL-encoded filenames like "Screenshot+2025-10-30+at+13.49.35.png"
                filename = filename.replace('+', ' ')
                self.current_image = filename
                
        elif tag == 'figcaption':
            self.in_caption = True
            
    def handle_endtag(self, tag):
        if tag == 'figure':
            if self.current_product:
                self.products.append(self.current_product.copy())
            self.in_figure = False
            self.current_product = {}
            self.current_link = ""
            self.current_caption = ""
            self.current_image = ""
            
        elif tag == 'a':
            self.in_link = False
            
        elif tag == 'figcaption':
            self.in_caption = False
            
    def handle_data(self, data):
        if self.in_caption:
            self.current_caption += data.strip()
            if self.current_caption:
                self.current_product['caption'] = self.current_caption
                self.current_product['link'] = self.current_link
                self.current_product['image'] = self.current_image

# HTML content from user
html_content = """<div class="gallery-grid-wrapper" style="grid-template-columns: repeat(4, 1fr); grid-column-gap: 

        1.55vw; grid-row-gap: 1.55vw;

        width: auto">

    

    <figure class="gallery-grid-item has-clickthrough" data-loaded="true" data-show="true">

      <div class="gallery-grid-item-wrapper">

        

          <a href="https://www.divertimenti.co.uk/collections/dinnerware/products/costa-nova-riviera-plate-27cm" target="_blank" rel="noopener" class="gallery-grid-image-link" data-no-animation="">

            

<img data-src="https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp" data-image="https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp" data-image-dimensions="400x400" data-image-focal-point="0.5,0.5" alt="Set of 8 Costa Nova Riviera Plate - Azure 27cm- £140" data-load="false" src="https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp" width="400" height="400" sizes="(max-width:768px)73.8375vw,(max-width:992px)48.45vw,35.756249999999994vw" style="display:block;object-position:50% 50%;object-fit:cover;width:100%;height:100%" srcset="https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp?format=100w 100w, https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp?format=300w 300w, https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp?format=500w 500w, https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp?format=750w 750w, https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp?format=1000w 1000w, https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp?format=1500w 1500w, https://images.squarespace-cdn.com/content/v1/68b8af507b5fe01134e5f415/7eff5f3c-4aff-4412-89e6-28605763d550/1113501_428a8d3c-d73e-4d48-bf0f-aa0f74119fce_400x.webp?format=2500w 2500w" loading="lazy" decoding="async" data-loader="sqs">

          </a>

        

      </div>

      

        

          <figcaption class="gallery-caption gallery-caption-grid-simple">

            <div class="gallery-caption-wrapper">

              <p class="gallery-caption-content preFade fadeIn" style="transition-timing-function: ease; transition-duration: 0.9s; transition-delay: 0.20597s;">Set of 8 Costa Nova Riviera Plate - Azure 27cm- £140</p>

            </div>

          </figcaption>

        

      

    </figure>"""

# Read the full HTML from a file or use the provided content
# For now, I'll create a script that processes the HTML

if __name__ == "__main__":
    # This will be expanded with full HTML
    print("Product extractor ready")

