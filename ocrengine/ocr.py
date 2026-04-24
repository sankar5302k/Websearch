import pytesseract
import cv2
import numpy as np
import fitz  

class UniversalOCR:
    def __init__(self, tesseract_cmd=None, lang='eng'):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.lang = lang

    def read_image(self, image_path):
        try:
            img = cv2.imread(image_path)
            img = self._preprocess(img)
            text = pytesseract.image_to_string(img, lang=self.lang)
            return text.strip()
        except Exception as e:
            return f"Error: {str(e)}"


    def read_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            full_text = []

            for i, page in enumerate(doc):
                pix = page.get_pixmap()
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

                img = self._preprocess(img)
                text = pytesseract.image_to_string(img, lang=self.lang)

                full_text.append(f"\n--- Page {i+1} ---\n{text}")

            return "\n".join(full_text).strip()

        except Exception as e:
            return f"Error: {str(e)}"

    def read(self, file_path):
        if file_path.lower().endswith(".pdf"):
            return self.read_pdf(file_path)
        return self.read_image(file_path)

    def _preprocess(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
        return gray