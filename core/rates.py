class Game:
    max_level: int
    upgrade_increment: int
    extra_roll_rate: float
    total_slots: int
    sub_weights: dict
    main_weights: list


class Genshin(Game):
    max_level = 20
    upgrade_increment = 4
    extra_roll_rate = 0.2
    total_slots = 5

    sub_weights = {
        "atk": 6,
        "def": 6,
        "hp": 6,
        "atk_p": 4,
        "def_p": 4,
        "hp_p": 4,
        "er": 4,
        "em": 4,
        "cr": 3,
        "cd": 3
    }

    main_weights = [
        {
            "hp": 1
        },
        {
            "atk": 1
        },
        {
            "hp_p": 8,
            "atk_p": 8,
            "def_p": 8,
            "er": 3,
            "em": 3
        },
        {
            "hp_p": 7.7,
            "atk_p": 7.7,
            "def_p": 7.6,
            "pyro": 2,
            "hydro": 2,
            "anemo": 2,
            "electro": 2,
            "dendro": 2,
            "cryo": 2,
            "geo": 2,
            "physical": 2,
            "em": 1
        },
        {
            "hp_p": 11,
            "atk_p": 11,
            "def_p": 11,
            "cr": 5,
            "cd": 5,
            "hb": 5,
            "em": 2
        }
    ]


class HSR(Game):
    max_level = 15
    upgrade_increment = 3
    extra_roll_rate = 0.2
    total_slots = 6

    sub_weights = {
        "atk": 10,
        "def": 10,
        "hp": 10,
        "atk_p": 10,
        "def_p": 10,
        "hp_p": 10,
        "spd": 4,
        "cr": 6,
        "cd": 6,
        "ehr": 8,
        "eff_res": 8,
        "be": 8
    }

    main_weights = [
        {
            "hp": 1,
        },
        {
            "atk": 1,
        },
        {
            "hp_p": 2,
            "def_p": 2,
            "atk_p": 2,
            "ehr": 1,
            "hb": 1,
            "cr": 1,
            "cd": 1,
        },
        {
            "hp_p": 14,
            "atk_p": 15,
            "def_p": 15,
            "spd": 6,
        },
        {
            "hp_p": 12,
            "atk_p": 13,
            "def_p": 12,
            "physical": 9,
            "fire": 9,
            "ice": 9,
            "lightning": 9,
            "wind": 9,
            "quantum": 9,
            "imaginary": 9,
        },
        {
            "hp_p": 26,
            "atk_p": 27,
            "def_p": 24,
            "be": 16,
            "er": 5,
        }
    ]


class ZZZ(Game):
    max_level = 15
    upgrade_increment = 3
    extra_roll_rate = 0.2
    total_slots = 6

    sub_weights = {
        "atk": 10,
        "def": 11,
        "hp": 11,
        "atk_p": 10,
        "def_p": 11,
        "hp_p": 11,
        "cr": 9,
        "cd": 9,
        "pen": 9,
        "ap": 9
    }

    main_weights = [
        {
            "hp": 1
        },
        {
            "atk": 1
        },
        {
            "def": 1
        },
        {
            "hp_p": 21,
            "atk_p": 18,
            "def_p": 21,
            "cr": 12,
            "cd": 12,
            "ap": 15
        },
        {
            "hp_p": 21,
            "atk_p": 18,
            "def_p": 21,
            "pen_r": 10,
            "fire": 6,
            "physical": 6,
            "ice": 6,
            "ether": 6,
            "electric": 6,
            "wind": 6  # Don't know how wind bonus affects other rates
        },
        {
            "hp_p": 21,
            "atk_p": 18,
            "def_p": 21,
            "impact": 15,
            "am": 15,
            "er": 10
        }
    ]


game_classes = {
    "genshin": Genshin,
    "hsr": HSR,
    "zzz": ZZZ
}
