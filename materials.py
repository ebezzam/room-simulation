materials_absorption_table = {
    "anechoic": {"description": "Anechoic material", "coeffs": [1.0]},
    # Massive constructions and hard surfaces
    "hard_surface": {
        "description": "Walls, hard surfaces average (brick walls, plaster, "
        "hard floors, etc.)",
        "coeffs": [0.02, 0.02, 0.03, 0.03, 0.04, 0.05, 0.05],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "brickwork": {
        "description": "Walls, rendered brickwork",
        "coeffs": [0.01, 0.02, 0.02, 0.03, 0.03, 0.04, 0.04],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "rough_concrete": {
        "description": "Rough concrete",
        "coeffs": [0.02, 0.03, 0.03, 0.03, 0.04, 0.07, 0.07],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "smooth_concrete": {
        "description": "Smooth unpainted concrete",
        "coeffs": [0.01, 0.01, 0.02, 0.02, 0.02, 0.05, 0.05],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "rough_limewash": {
        "description": "Rough lime wash",
        "coeffs": [0.02, 0.03, 0.04, 0.05, 0.04, 0.03, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "ceramic_tiles": {
        "description": "Ceramic tiles with a smooth surface",
        "coeffs": [0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "smooth_brickwork_painted": {
        "description": "Smooth brickwork with flush pointing, painted",
        "coeffs": [0.01, 0.01, 0.02, 0.02, 0.02, 0.02, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "smooth_brickwork_mortar": {
        "description": "Smooth brickwork, 10 mm deep pointing, pit sand "
        "mortar",
        "coeffs": [0.08, 0.09, 0.12, 0.16, 0.22, 0.24, 0.24],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "brick_wall": {
        "description": "Brick wall, stuccoed with a rough finish",
        "coeffs": [0.03, 0.03, 0.03, 0.04, 0.05, 0.07, 0.07],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "concrete_floor": {
        "description": "Concrete floor",
        "coeffs": [0.01, 0.03, 0.05, 0.02, 0.02, 0.02, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "marble_floor": {
        "description": "Marble floor",
        "coeffs": [0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    # Curtains
    "cotton_curtains": {
        "description": "Cotton curtains (0.5 kg/m2) draped to 3/4 area "
        "approx. 130 mm from wall",
        "coeffs": [0.30, 0.45, 0.65, 0.56, 0.59, 0.71, 0.71],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "curtains_hung": {
        "description": "Curtains (0.2 kg/m2) hung 90 mm from wall",
        "coeffs": [0.05, 0.06, 0.39, 0.63, 0.70, 0.73, 0.73],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "cotton_cloth": {
        "description": "Cotton cloth (0.33 kg/m2) folded to 7/8 area",
        "coeffs": [0.03, 0.12, 0.15, 0.27, 0.37, 0.42],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "densely_woven": {
        "description": "Densely woven window curtains 90 mm from wall",
        "coeffs": [0.06, 0.10, 0.38, 0.63, 0.70, 0.73],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "vertical_blinds": {
        "description": "Vertical blinds, 15 cm from wall, half opened "
        "(45 deg)",
        "coeffs": [0.03, 0.06, 0.13, 0.28, 0.49, 0.56],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "tight_velvet": {
        "description": "Tight velvet curtains",
        "coeffs": [0.05, 0.12, 0.35, 0.45, 0.38, 0.36, 0.36],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "curtain_fabric": {
        "description": "Curtain fabric, 15 cm from wall",
        "coeffs": [0.10, 0.38, 0.63, 0.52, 0.55, 0.65],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "curtain_fabric_folded": {
        "description": "Curtain fabric, folded, 15 cm from wall",
        "coeffs": [0.12, 0.60, 0.98, 1.0, 1.0, 1.0, 1.0],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "studio": {
        "description": "Studio curtains, 22 cm from wall",
        "coeffs": [0.36, 0.26, 0.51, 0.45, 0.62, 0.76],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    # Ceiling absorbers
    "plasterboard": {
        "description": "Plasterboard ceiling on battens with large air-space "
        "above",
        "coeffs": [0.20, 0.15, 0.10, 0.08, 0.04, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    # Wood
    "plywood": {
        "description": "Thin plywood panelling",
        "coeffs": [0.42, 0.21, 0.10, 0.08, 0.06, 0.06],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "audience_floor": {
        "description": "Audience floor, 2 layers, 33 mm on sleepers over "
        "concrete",
        "coeffs": [0.09, 0.06, 0.05, 0.05, 0.05, 0.04],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "stage_floor": {
        "description": "Wood, stage floor, 2 layers, 27 mm over airspace",
        "coeffs": [0.10, 0.07, 0.06, 0.06, 0.06, 0.06],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    # Glazing
    "single_pane": {
        "description": "Single pane of glass, 3 mm",
        "coeffs": [0.08, 0.04, 0.03, 0.03, 0.02, 0.02, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "glass_window": {
        "description": "Glass window, 0.68 kg/m2",
        "coeffs": [0.10, 0.05, 0.04, 0.03, 0.03, 0.03, 0.03],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "lead_glazing": {
        "description": "Lead glazing",
        "coeffs": [0.30, 0.20, 0.14, 0.10, 0.05, 0.05],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "double_glazing_thick": {
        "description": "Double glazing, 2-3 mm glass, >30 mm gap",
        "coeffs": [0.15, 0.05, 0.03, 0.03, 0.02, 0.02, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "double_glazing": {
        "description": "Double glazing, 2-3 mm glass, 10 mm gap",
        "coeffs": [0.10, 0.07, 0.05, 0.03, 0.02, 0.02, 0.02],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "double_glazing_lead": {
        "description": "Double glazing, lead on the inside",
        "coeffs": [0.15, 0.30, 0.18, 0.10, 0.05, 0.05],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    # Floor coverings
    "cotton_carpet": {
        "description": "Cotton carpet",
        "coeffs": [0.07, 0.31, 0.49, 0.81, 0.66, 0.54, 0.48],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "loop_pile_tufted_carpet": {
        "description": "Loop pile tufted carpet, 1.4 kg/m2, 9.5 mm pile "
        "height: On hair pad, 3.0 kg/m2",
        "coeffs": [0.10, 0.40, 0.62, 0.70, 0.63, 0.88],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "thin_carpet": {
        "description": "Thin carpet, cemented to concrete",
        "coeffs": [0.02, 0.04, 0.08, 0.20, 0.35, 0.40],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "6mm_carpet": {
        "description": "(Floor covering) 6 mm pile carpet bonded to "
        "closed-cell foam underlay",
        "coeffs": [0.03, 0.09, 0.25, 0.31, 0.33, 0.44, 0.44],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "6mm_carpet_open": {
        "description": "6 mm pile carpet bonded to open-cell foam underlay",
        "coeffs": [0.03, 0.09, 0.25, 0.31, 0.33, 0.44, 0.44],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "9mm_carpet": {
        "description": "9 mm tufted pile carpet on felt underlay",
        "coeffs": [0.08, 0.08, 0.30, 0.60, 0.75, 0.80, 0.80],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "needle_felt": {
        "description": "Needle felt 5 mm stuck to concrete",
        "coeffs": [0.02, 0.02, 0.05, 0.15, 0.30, 0.40, 0.40],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "10mm_carpet": {
        "description": "10 mm soft carpet on concrete",
        "coeffs": [0.09, 0.08, 0.21, 0.26, 0.27, 0.37],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "hairy_carpet": {
        "description": "Hairy carpet on 3 mm felt",
        "coeffs": [0.11, 0.14, 0.37, 0.43, 0.27, 0.25, 0.25],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "5mm_rubber_carpet": {
        "description": "5 mm rubber carpet on concrete",
        "coeffs": [0.04, 0.04, 0.08, 0.12, 0.10, 0.10],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "carpet_on_felt": {
        "description": "Carpet 1.35 kg/m2, on hair felt or foam rubber",
        "coeffs": [0.08, 0.24, 0.57, 0.69, 0.71, 0.73],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "cocos_fibre": {
        "description": "Cocos fibre roll felt, 29 mm thick (unstressed), "
        "reverse side clad with paper, 2.2 kg/m2, 2 Rayl",
        "coeffs": [0.10, 0.13, 0.22, 0.35, 0.47, 0.57],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
}


empty_seating_absorption_table = {
    # 2 seats per m2
    "wooden": {
        "description": "Wooden chairs without cushion",
        "coeffs": [0.05, 0.08, 0.10, 0.12, 0.12, 0.12],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "plastic": {
        "description": "Unoccupied plastic chairs",
        "coeffs": [0.06, 0.10, 0.10, 0.20, 0.30, 0.20, 0.20],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "medium_upholstered": {
        "description": "Medium upholstered concert chairs, empty",
        "coeffs": [0.49, 0.66, 0.80, 0.88, 0.82, 0.70],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "heavily_upholstered": {
        "description": "Heavily upholstered seats, unoccupied",
        "coeffs": [0.70, 0.76, 0.81, 0.84, 0.84, 0.81],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "cloth_upholstered": {
        "description": "Empty chairs, upholstered with cloth cover",
        "coeffs": [0.44, 0.60, 0.77, 0.89, 0.82, 0.70, 0.70],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "leather_upholstered": {
        "description": "Empty chairs, upholstered with leather cover",
        "coeffs": [0.40, 0.50, 0.58, 0.61, 0.58, 0.50, 0.50],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "moderately_upholstered": {
        "description": "Unoccupied, moderately upholstered chairs "
        "(0.90 m x 0.55 m)",
        "coeffs": [0.44, 0.56, 0.67, 0.74, 0.83, 0.87],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
}

materials_scattering_table = {
    "no_scattering": {"description": "No scattering", "coeffs": [0.0]},
    "rpg_skyline": {
        "description": "Diffuser RPG Skyline",
        "coeffs": [0.01, 0.08, 0.45, 0.82, 1.0],
        "center_freqs": [125, 250, 500, 1000, 2000],
    },
    "rpg_qrd": {
        "description": "Diffuser RPG QRD",
        "coeffs": [0.06, 0.15, 0.45, 0.95, 0.88, 0.91],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000],
    },
    "theatre_audience": {
        "description": "Theatre Audience",
        "coeffs": [0.3, 0.5, 0.6, 0.6, 0.7, 0.7, 0.7],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "classroom_tables": {
        "description": "Rows of classroom tables and persons on chairs",
        "coeffs": [0.2, 0.3, 0.4, 0.5, 0.5, 0.6, 0.6],
        "center_freqs": [125, 250, 500, 1000, 2000, 4000, 8000],
    },
    "amphitheatre_steps": {
        "description": "Amphitheatre steps, length 82 cm, height 30 cm "
        "(Farnetani 2005)",
        "coeffs": [0.05, 0.45, 0.75, 0.9, 0.9],
        "center_freqs": [125, 250, 500, 1000, 2000],
    },
}
