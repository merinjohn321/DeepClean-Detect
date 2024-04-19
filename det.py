import cv2
import numpy as np
# import dark_channel_prior as dcp
import underwaterApp.gan as dcp
import underwaterApp.inference as inf

# Function to remove noise from an image
def remove_noise(image):
    # Replace this with your noise removal code
    processed_image, alpha_map = dcp.haze_removal_gan(image, w_size=15, a_omega=0.95, gf_w_size=200, eps=1e-6)
    # processed_image, alpha_map = dcp.haze_removal(image, w_size=15, a_omega=0.95, gf_w_size=200, eps=1e-6)
    return processed_image

# Function to perform object detection on an image
def detect_objects(image):
    # Replace this with your object detection code
    # Make sure the output image has bounding boxes around the detected objects
    output_image, class_names = inf.detect(image)
    return output_image, class_names

# Main function
def main(img):
    # Load an image
    image_path = f"E:\\PYTHON\\Underwater\\static\\media\\{img}"  # Provide the path to your image
    input_image = cv2.imread(image_path)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    input_image = cv2.resize(input_image, (416, 416))

    # Process the input
    processed_image = remove_noise(input_image)

    # Run the model
    output_image, class_names = detect_objects(processed_image)
    class_names = set(class_names)
    class_names = list(class_names)
    result = ''
    if len(class_names) > 1:
        for c in class_names:
            cl = str(c)
            cl = cl.title()
            result += f"{cl} Detected   "
    else:
        cl = class_names[0]
        cl = cl.title()
        result = f"{cl} Detected"
    cv2.imshow("Output Image", cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))
    cv2.imshow("Inputted Image", cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return result


