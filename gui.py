import tkinter as tk
from tkinter import filedialog, messagebox
from encryption import encrypt_file, decrypt_file
from key_management import generate_rsa_keys
from file_utils import secure_delete
import os

def browse_file(title):
    return filedialog.askopenfilename(title=title)

def save_rsa_keys(private_key, public_key):
    keys_folder = "keys"
    os.makedirs(keys_folder, exist_ok=True)
    with open(os.path.join(keys_folder, "private_key.pem"), "wb") as f:
        f.write(private_key)
    with open(os.path.join(keys_folder, "public_key.pem"), "wb") as f:
        f.write(public_key)

def start_gui():
    if not os.path.exists("keys/private_key.pem") or not os.path.exists("keys/public_key.pem"):
        private_key, public_key = generate_rsa_keys()
        save_rsa_keys(private_key, public_key)

    root = tk.Tk()
    root.title("CryptBuddy v1.0")
    root.geometry("400x500")
    root.minsize(350, 400)
    root.configure(bg="#f0f0f0")
    root.resizable(True, True)

    font_style = ("Arial", 12)
    root.option_add("*Font", font_style)

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(fill="both", expand=True)

    try:
        image_path = os.path.join(os.path.dirname(__file__), "buddy.png")
        image = tk.PhotoImage(file=image_path)
        smaller_image = image.subsample(5, 5)
        img_label = tk.Label(frame, image=smaller_image, bg="#f0f0f0")
        img_label.image = smaller_image
        img_label.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Image could not be loaded: {e}")

    def on_encrypt():
        file_path = browse_file("Select file to encrypt")
        if file_path:
            key_path = browse_file("Select recipient's public key")
            if key_path:
                try:
                    with open(key_path, "rb") as f:
                        pubkey = f.read()
                    encrypt_file(file_path, pubkey)
                    messagebox.showinfo("Success", f"Encrypted: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Encryption failed:\n{e}")

    def on_decrypt():
        file_path = browse_file("Select file to decrypt")
        if file_path:
            private_key_path = browse_file("Select your private key")
            if private_key_path:
                try:
                    with open(private_key_path, "rb") as key_file:
                        private_key = key_file.read()
                    plaintext = decrypt_file(file_path, private_key)

                    if file_path.lower().endswith(".txt"):
                        try:
                            messagebox.showinfo("Decrypted Content", plaintext.decode("utf-8"))
                        except UnicodeDecodeError:
                            messagebox.showwarning("Partially Decoded", "File decrypted, but cannot be fully displayed as text.")
                    else:
                        save_path = filedialog.asksaveasfilename(
                            title="Save decrypted file as",
                            defaultextension="",
                            initialfile=os.path.basename(file_path).replace(".enc", "")
                        )
                        if save_path:
                            with open(save_path, "wb") as f:
                                f.write(plaintext)
                            messagebox.showinfo("Decryption Complete", f"Decrypted file saved to:\n{save_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Decryption failed:\n{e}")

    def on_secure_delete():
        file_path = browse_file("Select file to securely delete")
        if file_path:
            try:
                secure_delete(file_path)
                messagebox.showinfo("Deleted", f"Securely deleted: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Deletion failed:\n{e}")

    button_style = {"padx": 10, "pady": 5, "width": 28}
    tk.Button(frame, text="Encrypt File", command=on_encrypt, **button_style).pack(pady=5)
    tk.Button(frame, text="Decrypt File", command=on_decrypt, **button_style).pack(pady=5)
    tk.Button(frame, text="Securely Delete File", command=on_secure_delete, **button_style).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
