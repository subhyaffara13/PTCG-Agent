import fitz
import os
import re

def main():
    pdf_path = "skills/card_pool_reference.pdf"
    output_dir = "visualizer/images"
    os.makedirs(output_dir, exist_ok=True)

    print("Opening PDF...")
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Total pages: {total_pages}")

    # Map card IDs to PDF pages
    # First, let's parse the index pages. We know index pages are pages 0 to 38.
    card_to_page = {}
    
    print("Parsing index pages...")
    for page_idx in range(39):
        page = doc[page_idx]
        text_lines = [line.strip() for line in page.get_text().split("\n") if line.strip()]
        links = page.get_links()

        # Let's filter links pointing to a page in the document (kind=1)
        target_links = [l for l in links if l.get("kind") == 1]
        
        # Parse the rows. Each row has: Card ID, Name, Expansion, Coll No, View Image
        # We can find integers in text_lines that represent Card IDs.
        # Let's match the number of target links with the sequence of Card IDs.
        # In the page text, Card ID is followed by the name, expansion, etc.
        # Let's find all rows by looking for 'View Image'
        view_image_indices = [i for i, line in enumerate(text_lines) if line == "View Image"]
        
        for idx, view_idx in enumerate(view_image_indices):
            # The Card ID should be 4 positions before 'View Image'
            card_id_idx = view_idx - 4
            if card_id_idx >= 0:
                card_id_str = text_lines[card_id_idx]
                # Verify it is a valid integer Card ID
                if card_id_str.isdigit():
                    card_id = int(card_id_str)
                    if idx < len(target_links):
                        target_page = target_links[idx].get("page")
                        if target_page:
                            card_to_page[card_id] = target_page

    print(f"Mapped {len(card_to_page)} cards to pages.")

    # Extract images from mapped pages
    print("Extracting images...")
    extracted_count = 0
    for card_id, page_num in card_to_page.items():
        if page_num >= total_pages:
            continue
            
        page = doc[page_num]
        image_list = page.get_images()
        
        if image_list:
            # Get the first image on the page
            xref = image_list[0][0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            output_filename = f"card_{card_id}.{image_ext}"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            
            extracted_count += 1
            if extracted_count % 100 == 0:
                print(f"Extracted {extracted_count} images...")

    print(f"Completed! Extracted {extracted_count} card images to {output_dir}")

if __name__ == "__main__":
    main()
