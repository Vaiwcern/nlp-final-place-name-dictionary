import os
import fitz  # PyMuPDF
import logging
import argparse

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def extract_image_and_text_from_pdf(pdf_path, start_page=1, result_path="output"):
    try:
        # Mở file PDF
        pdf_document = fitz.open(pdf_path)
        file_name_no_ext = os.path.splitext(os.path.basename(pdf_path))[0]

        output_folder = os.path.join(result_path, file_name_no_ext)  # Đặt tên thư mục kết quả
        if os.path.exists(output_folder):
            logging.info(f"Folder '{file_name_no_ext}' already exists. Skipping processing.")
            return  # Nếu thư mục đã tồn tại, bỏ qua

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Mở file content.txt để ghi nội dung
        content_file_path = os.path.join(output_folder, "content.txt")
        with open(content_file_path, "w", encoding="utf-8") as content_file:

            # Duyệt qua các trang bắt đầu từ start_page
            for page_index in range(start_page-1, pdf_document.page_count):
                try:
                    page = pdf_document.load_page(page_index)  # Tải trang
                    logging.info(f"Extracting text from file: {file_name_no_ext}, Page: {page_index + 1}")

                    # Lấy chiều cao của trang
                    page_height = page.rect.height
                    header_height = 0
                    footer_height = page_height * 0.1  # Bỏ qua 10% cuối trang

                    # Định nghĩa vùng lấy văn bản (loại bỏ header/footer)
                    text_area = fitz.Rect(
                        0,  # trái
                        header_height,  # trên
                        page.rect.width,  # phải
                        page.rect.height - footer_height  # dưới
                    )

                    text = page.get_text("text", clip=text_area)

                    # Ghi nội dung văn bản vào content.txt
                    # content_file.write(f"Page {page_index + 1}:\n")
                    content_file.write(text)
                    content_file.write("\n")  # Thêm dòng trống giữa các trang

                except Exception as e:
                    logging.error(f"Error extracting text from page {page_index + 1} of file '{file_name_no_ext}': {str(e)}")

        pdf_document.close()
        logging.info("Text extraction completed.")
    
    except Exception as e:
        logging.error(f"Error processing file '{pdf_path}': {str(e)}")

if __name__ == "__main__":
    try:
    # Set up command line argument parsing
        parser = argparse.ArgumentParser(description="Extract text from PDF pages and save them as a single text file.")
        parser.add_argument("pdf_path", help="Path to the PDF file")
        parser.add_argument("output_folder", help="Path to the output folder")
        parser.add_argument("--start_page", type=int, default=1, help="Page to start extraction from (default is 1)")

        # Parse the arguments
        args = parser.parse_args()

        # Call the function with the provided arguments
        extract_image_and_text_from_pdf(args.pdf_path, start_page=args.start_page, result_path=args.output_folder)

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
