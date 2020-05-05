materials_absorption_table = {
    "hard_surface": {
        "description": "Walls, hard surfaces average (brick walls, plaster, "
        "hard floors, etc.)",
        "coeffs": [0.02, 0.02, 0.03, 0.03, 0.04, 0.05, 0.05],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "ceramic_tiles": {
        "description": "Ceramic tiles with a smooth surface",
        "coeffs": [0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "glass_window": {
        "description": "Glass window, 0.68 kg/m2",
        "coeffs": [0.10, 0.05, 0.04, 0.03, 0.03, 0.03, 0.03],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "thin_carpet": {
        "description": "Thin carpet, cemented to concrete",
        "coeffs": [0.02, 0.04, 0.08, 0.20, 0.35, 0.40],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "cotton_cloth": {
        "description": "Cotton cloth (0.33 kg/m2) folded to 7/8 area",
        "coeffs": [0.03, 0.12, 0.15, 0.27, 0.37, 0.42],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "plasterboard": {
        "description": "Plasterboard ceiling on battens with large air-space "
        "above",
        "coeffs": [0.20, 0.15, 0.10, 0.08, 0.04, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "vertical_blinds": {
        "description": "Vertical blinds, 15 cm from wall, half opened "
        "(45 deg)",
        "coeffs": [0.03, 0.06, 0.13, 0.28, 0.49, 0.56],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "smooth_concrete": {
        "description": "Smooth unpainted concrete",
        "coeffs": [0.01, 0.01, 0.02, 0.02, 0.02, 0.05, 0.05],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "plywood": {
        "description": "Thin plywood panelling",
        "coeffs": [0.42, 0.21, 0.10, 0.08, 0.06, 0.06],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "curtains_hung": {
        "description": "Curtains (0.2 kg/m2) hung 90 mm from wall",
        "coeffs": [0.05, 0.06, 0.39, 0.63, 0.70, 0.73, 0.73],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
}
