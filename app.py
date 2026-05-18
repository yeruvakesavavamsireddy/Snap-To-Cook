import streamlit as st
from PIL import Image
from inference import generate_recipe
from db import save_recipe, fetch_recipes, delete_recipe
import streamlit.components.v1 as components
import os


st.set_page_config(page_title="SnapToCook 🍳", layout="wide")


# -----------------------------
# BROWSER VOICE FUNCTIONS
# -----------------------------

def speak_browser(text, rate=1):

    js_code = f"""
    <script>
        var synth = window.speechSynthesis;
        synth.cancel();

        var utterance = new SpeechSynthesisUtterance(`{text}`);
        utterance.rate = {rate};

        synth.speak(utterance);
    </script>
    """

    components.html(js_code, height=0)


def stop_browser_voice():

    js_code = """
    <script>
        window.speechSynthesis.cancel();
    </script>
    """

    components.html(js_code, height=0)


# -----------------------------
# SIDEBAR MENU
# -----------------------------

menu = st.sidebar.selectbox(
    "Menu",
    ["Generate Recipe", "Saved Recipes"]
)


# =============================
# GENERATE RECIPE PAGE
# =============================

if menu == "Generate Recipe":

    st.title("📸 SnapToCook")

    img = st.file_uploader(
        "Upload food image",
        type=["jpg", "jpeg", "png"]
    )

    if img:

        image = Image.open(img)

        st.image(image, width=700)

        if st.button("Generate Recipe"):

            try:

                title, ingredients, steps, confidence, similarity, ref_img = generate_recipe(
                    image, img.name
                )

                st.session_state["recipe"] = (title, ingredients, steps)
                st.session_state["metrics"] = (confidence, similarity)
                st.session_state["ref_img"] = ref_img

                # -----------------------------
                # BUILD VOICE TEXT
                # -----------------------------

                voice_text = f"Recipe Title. {title}. "

                voice_text += "Ingredients are. "

                for item in ingredients:
                    voice_text += f"{item}. "

                voice_text += "Now the cooking instructions. "

                for i, step in enumerate(steps, 1):
                    voice_text += f"Step {i}. {step}. "

                st.session_state["voice_text"] = voice_text

            except Exception as e:

                st.error("❌ Failed to generate recipe.")
                st.exception(e)

        # -----------------------------
        # SHOW RESULT
        # -----------------------------

        if "recipe" in st.session_state:

            title, ingredients, steps = st.session_state["recipe"]
            confidence, similarity = st.session_state["metrics"]
            ref_img = st.session_state["ref_img"]

            st.subheader("🍽️ Recipe Title")
            st.write(title)

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"🎯 Model Confidence: {confidence}%")

            with col2:
                st.info(f"🔎 Similarity Score: {similarity}%")

            # -----------------------------
            # SHOW REFERENCE IMAGE
            # -----------------------------

            if ref_img and os.path.exists(ref_img):

                st.subheader("📷 Most Similar Dish from Dataset")

                st.image(ref_img, width=400)

            # -----------------------------
            # INGREDIENTS
            # -----------------------------

            st.subheader("🧾 Ingredients")

            for item in ingredients:
                st.write("-", item)

            # -----------------------------
            # INSTRUCTIONS
            # -----------------------------

            st.subheader("👨‍🍳 Instructions")

            for idx, step in enumerate(steps, 1):
                st.write(f"{idx}. {step}")

            st.divider()

            # -----------------------------
            # VOICE CONTROLS
            # -----------------------------

            st.subheader("🎙️ Voice Assistant")

            if "voice_speed" not in st.session_state:
                st.session_state.voice_speed = 1.0

            st.session_state.voice_speed = st.slider(
                "🎚 Voice Speed",
                0.5,
                2.0,
                st.session_state.voice_speed,
                0.1
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("🔊 Read Recipe"):

                    if "voice_text" in st.session_state:

                        speak_browser(
                            st.session_state["voice_text"],
                            rate=st.session_state.voice_speed
                        )

                    else:
                        st.warning("Generate recipe first.")

            with col2:

                if st.button("⏹ Stop Voice"):
                    stop_browser_voice()

            st.divider()

            # -----------------------------
            # SAVE RECIPE
            # -----------------------------

            if st.button("💾 Save Recipe"):

                success = save_recipe(title, ingredients, steps)

                if success:
                    st.success("✅ Recipe saved to database!")

                else:
                    st.error("❌ Failed to save recipe")


# =============================
# SAVED RECIPES PAGE
# =============================

elif menu == "Saved Recipes":

    st.title("📚 Saved Recipes")

    recipes = fetch_recipes()

    if not recipes:

        st.info("No recipes saved yet.")

    else:

        for r in recipes:

            recipe_id, title, ingredients, instructions = r

            st.subheader(title)

            st.text("Ingredients:\n" + ingredients)

            st.text("Instructions:\n" + instructions)

            if st.button(
                f"Delete '{title}'",
                key=f"delete_{recipe_id}"
            ):

                success = delete_recipe(recipe_id)

                if success:

                    st.success(f"🗑️ Deleted: {title}")

                    st.rerun()

                else:

                    st.error("❌ Failed to delete recipe")

            st.markdown("---")