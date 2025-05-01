from graph import workflow
import matplotlib.pyplot as plt
from PIL import Image
import io

# Assuming graph.get_graph().draw_mermaid_png() generates the PNG image data
graph_image_data = workflow.get_graph().draw_mermaid_png()

# Convert image data to PIL image for displaying
image = Image.open(io.BytesIO(graph_image_data))

# Show the image using matplotlib
plt.imshow(image)
plt.axis('off')  # Hide axes for a cleaner look
plt.show()
