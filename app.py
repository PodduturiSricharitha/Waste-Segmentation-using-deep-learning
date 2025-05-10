from flask import Flask, render_template, request
from ultralytics import YOLO
import os
from PIL import Image

app = Flask(__name__)

# Load YOLO model once
model = YOLO("model/best.pt")

# Disposal rules dictionary (rule-based system)
disposal_rules = {
        "1-PET-Polyethylene_Terephthalate": (
            "♻️ <strong>Type:</strong> PET (Polyethylene Terephthalate)<br>"
            "🔄 <strong>Common Uses:</strong> Water bottles, soda bottles, food containers.<br>"
            "🧽 <strong>Disposal:</strong> Rinse thoroughly to remove any food or liquid residue. "
            "Remove caps and labels if possible.<br>"
            "📦 <strong>Recycling:</strong> Place in the plastic recycling bin (usually labeled with '1'). "
            "Flatten bottles to save space.<br>"
            "💡 <strong>Note:</strong> Highly recyclable and accepted in most curbside programs."
        ),
        "2-HDPE-High-Density_Polyethylene": (
            "♻️ <strong>Type:</strong> HDPE (High-Density Polyethylene)<br>"
            "🔄 <strong>Common Uses:</strong> Milk jugs, detergent bottles, shampoo bottles, grocery bags.<br>"
            "🧽 <strong>Disposal:</strong> Rinse and dry. Remove caps/lids if possible.<br>"
            "📦 <strong>Recycling:</strong> Place in the plastic recycling bin (usually labeled with '2').<br>"
            "💡 <strong>Note:</strong> Widely recyclable due to its durability."
        ),
        "3-PVC-Polyvinyl_Chloride": (
            "♻️ <strong>Type:</strong> PVC (Polyvinyl Chloride)<br>"
            "🔄 <strong>Common Uses:</strong> Pipes, cling film, blister packaging.<br>"
            "🚫 <strong>Disposal:</strong> Do NOT burn. Toxic fumes are released.<br>"
            "📍 <strong>Recycling:</strong> Check local recycling centers for PVC acceptance. "
            "Otherwise, dispose of responsibly in general waste if no recycling option is available.<br>"
            "💡 <strong>Note:</strong> Difficult to recycle due to its composition."
        ),
        "4-LDPE-Low-Density_Polyethylene": (
            "♻️ <strong>Type:</strong> LDPE (Low-Density Polyethylene)<br>"
            "🔄 <strong>Common Uses:</strong> Plastic bags, bread bags, shrink wraps, squeezable bottles.<br>"
            "🧺 <strong>Disposal:</strong> Clean and dry.<br>"
            "📦 <strong>Recycling:</strong> Not accepted in regular curbside recycling. "
            "Take to soft plastic collection points (e.g., supermarkets).<br>"
            "💡 <strong>Note:</strong> Reuse bags when possible to reduce waste."
        ),
        "5-PP-Polypropylene": (
            "♻️ <strong>Type:</strong> PP (Polypropylene)<br>"
            "🔄 <strong>Common Uses:</strong> Yogurt containers, bottle caps, straws, food packaging.<br>"
            "🧽 <strong>Disposal:</strong> Rinse to remove food residue.<br>"
            "📦 <strong>Recycling:</strong> Accepted by many recycling programs. Check local guidelines.<br>"
            "💡 <strong>Note:</strong> Durable and often used in reusable containers."
        ),
        "6-PS-Polystyrene": (
            "♻️ <strong>Type:</strong> PS (Polystyrene/Styrofoam)<br>"
            "🔄 <strong>Common Uses:</strong> Disposable cutlery, foam packaging, takeout containers.<br>"
            "🚫 <strong>Disposal:</strong> Difficult to recycle. Avoid breaking into smaller pieces.<br>"
            "📍 <strong>Recycling:</strong> Take to specialized recycling centers if available, otherwise dispose of in general waste.<br>"
            "💡 <strong>Note:</strong> Consider alternatives due to environmental impact."
        ),
        "Can": (
            "♻️ <strong>Type:</strong> Metal (Aluminum/Steel Can)<br>"
            "🔄 <strong>Common Uses:</strong> Beverage cans, food tins.<br>"
            "🧽 <strong>Disposal:</strong> Rinse to remove food residue.<br>"
            "📦 <strong>Recycling:</strong> Place in the metal recycling bin. "
            "Flatten cans if possible to save space.<br>"
            "💡 <strong>Note:</strong> Highly recyclable with significant energy savings."
        ),
        "Carton": (
            "♻️ <strong>Type:</strong> Carton (TetraPak)<br>"
            "🔄 <strong>Common Uses:</strong> Juice cartons, milk cartons, soup boxes.<br>"
            "🧽 <strong>Disposal:</strong> Rinse and flatten to save space.<br>"
            "📦 <strong>Recycling:</strong> Check if your local facility accepts cartons. "
            "Some areas require dropping off at dedicated carton recycling points.<br>"
            "💡 <strong>Note:</strong> Composed of mixed materials (paper, plastic, aluminum)."
        ),
        "E-Waste": (
            "⚡ <strong>Type:</strong> Electronic Waste (E-Waste)<br>"
            "🔄 <strong>Common Uses:</strong> Phones, chargers, laptops, batteries.<br>"
            "🚫 <strong>Disposal:</strong> Do NOT throw in regular trash due to hazardous components.<br>"
            "📍 <strong>Recycling:</strong> Take to an authorized e-waste recycling facility or designated drop-off point.<br>"
            "💡 <strong>Note:</strong> Many electronics retailers have e-waste collection programs."
        ),
        "Glass": (
            "♻️ <strong>Type:</strong> Glass<br>"
            "🔄 <strong>Common Uses:</strong> Jars, glass containers, non-bottle glass items.<br>"
            "🧽 <strong>Disposal:</strong> Rinse and remove lids or caps.<br>"
            "📦 <strong>Recycling:</strong> Place in glass recycling bins (separated by color if required).<br>"
            "💡 <strong>Note:</strong> Avoid disposing of broken glass in recycling bins; wrap in newspaper and dispose safely."
        ),
        "Glass Bottle": (
            "♻️ <strong>Type:</strong> Glass Bottle<br>"
            "🔄 <strong>Common Uses:</strong> Beverage bottles (e.g., wine, soda).<br>"
            "🧽 <strong>Disposal:</strong> Rinse thoroughly and remove caps.<br>"
            "📦 <strong>Recycling:</strong> Place in appropriate glass recycling bin.<br>"
            "💡 <strong>Note:</strong> Glass is 100% recyclable without loss of quality."
        ),
        "Medical Mask": (
            "⚠️ <strong>Type:</strong> Medical Waste<br>"
            "🔄 <strong>Common Uses:</strong> Disposable masks, gloves.<br>"
            "🚫 <strong>Disposal:</strong> Do NOT recycle. Place in a sealed bag to prevent contamination.<br>"
            "📍 <strong>Recycling:</strong> Dispose of in designated medical waste or general waste if no other option is available.<br>"
            "💡 <strong>Note:</strong> Always sanitize hands after handling."
        ),
        "Metal": (
            "♻️ <strong>Type:</strong> Metal<br>"
            "🔄 <strong>Common Uses:</strong> Cans, scrap metal, kitchen utensils.<br>"
            "🧽 <strong>Disposal:</strong> Clean off food residues if applicable.<br>"
            "📦 <strong>Recycling:</strong> Place in metal recycling bins or take to a scrap metal recycling center.<br>"
            "💡 <strong>Note:</strong> Metals are infinitely recyclable."
        ),
        "Organic Waste": (
            "🌿 <strong>Type:</strong> Organic Waste<br>"
            "🔄 <strong>Common Uses:</strong> Food scraps, yard waste.<br>"
            "🧺 <strong>Disposal:</strong> Separate from non-organic waste.<br>"
            "📦 <strong>Recycling:</strong> Compost at home or place in a green bin for municipal composting.<br>"
            "💡 <strong>Note:</strong> Reduces landfill waste and enriches soil when composted."
        ),
        "Phone Case": (
            "⚡ <strong>Type:</strong> E-Waste/Plastic<br>"
            "🔄 <strong>Common Uses:</strong> Phone covers (plastic, silicone).<br>"
            "🧺 <strong>Disposal:</strong> Check for take-back programs from manufacturers or retailers.<br>"
            "📍 <strong>Recycling:</strong> Some cases can be recycled via special programs, otherwise dispose of responsibly in general waste.<br>"
            "💡 <strong>Note:</strong> Consider donating if in good condition."
        ),
        "Plastic Bottle": (
            "♻️ <strong>Type:</strong> Plastic Bottle<br>"
            "🔄 <strong>Common Uses:</strong> Beverage bottles, cleaning product bottles.<br>"
            "🧽 <strong>Disposal:</strong> Empty, rinse, and remove caps.<br>"
            "📦 <strong>Recycling:</strong> Place in plastic recycling bin.<br>"
            "💡 <strong>Note:</strong> Flatten bottles to save space."
        ),
        "Plastic Brush": (
            "🚫 <strong>Type:</strong> Plastic<br>"
            "🔄 <strong>Common Uses:</strong> Toothbrushes, cleaning brushes.<br>"
            "🧺 <strong>Disposal:</strong> Not widely recyclable due to mixed materials.<br>"
            "📍 <strong>Recycling:</strong> Check if specialized recycling programs (like TerraCycle) are available.<br>"
            "💡 <strong>Note:</strong> Replace with eco-friendly alternatives where possible."
        ),
        "Plastic bag": (
            "♻️ <strong>Type:</strong> Plastic Bag<br>"
            "🔄 <strong>Common Uses:</strong> Grocery bags, packaging bags.<br>"
            "🧺 <strong>Disposal:</strong> Keep clean and dry for recycling.<br>"
            "📦 <strong>Recycling:</strong> Take to plastic bag collection points (often found at supermarkets).<br>"
            "💡 <strong>Note:</strong> Reuse bags whenever possible to minimize waste."
        ),
        "Plastics": (
            "♻️ <strong>Type:</strong> Mixed Plastics<br>"
            "🔄 <strong>Common Uses:</strong> Various household plastic items.<br>"
            "🧽 <strong>Disposal:</strong> Clean and sort according to resin codes if available.<br>"
            "📦 <strong>Recycling:</strong> Follow local recycling guidelines for each type of plastic.<br>"
            "💡 <strong>Note:</strong> Reducing plastic use can significantly help the environment."
        ),
        "Styrofoam": (
            "🚫 <strong>Type:</strong> Styrofoam (Polystyrene)<br>"
            "🔄 <strong>Common Uses:</strong> Foam cups, food containers, packing materials.<br>"
            "🚮 <strong>Disposal:</strong> Not accepted in regular recycling programs. "
            "Dispose of in general waste or take to specialized recycling centers if available.<br>"
            "💡 <strong>Note:</strong> Avoid using Styrofoam products to reduce environmental impact."
        ),
        "Wooden Waste": (
            "🌿 <strong>Type:</strong> Wood<br>"
            "🔄 <strong>Common Uses:</strong> Broken furniture, wooden pallets.<br>"
            "🧺 <strong>Disposal:</strong> Keep untreated wood separate from treated/painted wood.<br>"
            "📍 <strong>Recycling:</strong> Compost untreated wood or take to wood recycling centers. "
            "Treated wood should go to designated disposal facilities.<br>"
            "💡 <strong>Note:</strong> Reuse or repurpose if possible."
        ),
        "paper": (
            "♻️ <strong>Type:</strong> Paper<br>"
            "🔄 <strong>Common Uses:</strong> Newspapers, office paper, cardboard.<br>"
            "🧽 <strong>Disposal:</strong> Ensure paper is clean and dry. Remove tape or staples if possible.<br>"
            "📦 <strong>Recycling:</strong> Place in the paper recycling bin.<br>"
            "💡 <strong>Note:</strong> Avoid recycling greasy paper (e.g., pizza boxes); compost if possible."
        )
    }

def run_model(image_path):
    results = model(image_path)
    class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
    classes = set([model.names[c] for c in class_ids])

    # Save annotated image
    annotated_path = image_path.replace('.jpg', '_annotated.jpg')
    results[0].save(filename=annotated_path)

    return list(classes), annotated_path

def rule_based_instructions(classes):
    instructions = {}
    for cls in classes:
        instructions[cls] = disposal_rules.get(cls, "No rule available.")
    return instructions

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        save_path = os.path.join("static", "uploads", filename)
        file.save(save_path)

        # Run model and get results
        classes, annotated_path = run_model(save_path)

        # Get disposal instructions
        instructions = rule_based_instructions(classes)

        # Convert paths to static for rendering
        image_path = f"/static/uploads/{os.path.basename(annotated_path)}"
        return render_template('index.html', image_path=image_path, classes=classes, instructions=instructions)

    return render_template('index.html', image_path=None, classes=None, instructions=None)

if __name__ == '__main__':
    os.makedirs(os.path.join("static", "uploads"), exist_ok=True)
    app.run(debug=True)
