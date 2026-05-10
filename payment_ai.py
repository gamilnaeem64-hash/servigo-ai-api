import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
def check_if_receipt(text):

    receipt_keywords = [
        'total', 'amount', 'tax', 'invoice', 'receipt', 'cashier', 'price', 'sum',
        'فاتورة', 'إجمالي', 'مجموع', 'ضريبة', 'كاشير', 'السعر', 'الصافي', 'المدفوع'
    ]

    text_lower = text.lower()

    found_keywords = [word for word in receipt_keywords if word in text_lower]

    if len(found_keywords) > 0:
        return True, found_keywords

    return False, []


def verify_receipt(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return {
            "valid": False,
            "error": "image not readable"
        }

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    extracted_text = pytesseract.image_to_string(gray, lang='ara+eng')

    is_receipt, words = check_if_receipt(extracted_text)

    return {
        "valid": is_receipt,
        "keywords_found": words,
        "text": extracted_text
    }