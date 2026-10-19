"""Stop-lists for the Finnish word game «Sanamaailma» (no religion / mythology / afterlife / magic; plus profanity, adult, drugs, alcohol, death).
Used by lexicon.py / build_game.py / scan_religion.py: such words are kept out of crosswords, daily puzzles, bonus words, word of the day and cards.
Checked both on the Finnish word and on its Russian translation."""
import re
# Finnish religious vocabulary (exact words); stems in STOP_RE
STOP_WORDS = {
    'jumala', 'jumalat', 'jumalan', 'luoja', 'herra', 'kirkko', 'kappeli', 'katedraali', 'tuomiokirkko', 'temppeli', 'moskeija', 'synagoga', 'luostari',
    'enkeli', 'arkkienkeli', 'piru', 'paholainen', 'perkele', 'saatana', 'hiisi', 'demoni', 'riivaaja', 'helvetti', 'kadotus', 'paratiisi', 'taivasten',
    'risti', 'ristiä', 'krusifiksi', 'ristinmerkki', 'rukous', 'rukoilla', 'rukoili', 'rukoile', 'synti', 'syntinen', 'syntiä', 'pyhä', 'pyhimys', 'pyhäkkö', 'pyhitys',
    'pappi', 'piispa', 'arkkipiispa', 'paavi', 'nunna', 'kanttori', 'lukkari', 'diakoni', 'pastori', 'rovasti', 'kirkkoherra', 'imaami', 'rabbi',
    'raamattu', 'evankeliumi', 'psalmi', 'virsi', 'koraani', 'messu', 'jumalanpalvelus', 'alttari', 'saarna', 'saarnata', 'saarnaaja', 'kastaa', 'ehtoollinen',
    'rippi', 'rippikoulu', 'konfirmaatio', 'siunata', 'siunaus', 'kirota', 'kirous', 'kirottu', 'usko', 'uskonto', 'uskonnollinen', 'uskova', 'uskovainen', 'ateisti',
    'joulu', 'pääsiäinen', 'helluntai', 'loppiainen', 'pyhäinpäivä', 'kristitty', 'kristus', 'jeesus', 'kristinusko', 'kristillinen', 'luterilainen', 'ortodoksi',
    'katolinen', 'islam', 'muslimi', 'juutalainen', 'buddha', 'pakana', 'pakanallinen', 'epäjumala', 'sielu', 'sielut', 'aave', 'kummitus', 'haamu',
    'noita', 'noituus', 'noitua', 'taika', 'taikuri', 'taikoa', 'loitsu', 'loitsia', 'shamaani', 'tietäjä', 'ennustaja', 'ennustaa', 'ennustus', 'horoskooppi',
    'hauta', 'haudata', 'hautajaiset', 'hautausmaa', 'kalmisto', 'ruumis', 'vainaja', 'arkku', 'ikoni', 'pyhiinvaellus', 'apostoli', 'profeetta', 'messias',
    'marttyyri', 'ihme', 'ihmeitä', 'armo', 'pelastus', 'lunastus', 'tuomiopäivä', 'ylösnousemus', 'seurakunta', 'hurskas', 'jumalaton',
    'tonttu', 'menninkäinen', 'peikko', 'keiju', 'vampyyri', 'lohikäärme', 'ukko', 'tapio', 'ahti',
}
STOP_RE = re.compile(r'^(?:jumal|kirkko|kirkon|kirkoi|kirkoss|enkel|perkel|saatan|helvet|paratiis|ristiinnaul|rukoil|rukou|synti|pyhi|pyhä|pappi|pappe|papi|piisp|paavi|nunn|'
                     r'raamat|evankel|psalm|virre|alttar|saarn|siuna|kirou|kirot|uskon|kristi|kristu|jeesu|luteril|ortodoks|katolil|islam|musliim|pakan|epäjumal|'
                     r'sielu|aave|kummit|haam|noid|noit|taikuu|taika|taiko|loits|shamaan|ennust|haud|hauta|ruumii|vainaj|apostol|profeet|marttyyr|seurakun|hursk)')
# Russian clue patterns (word-boundary aware, so богатый / крестьянин / огрех / черта / культура don't match)
GLOSS_RE = re.compile(r'(?<![а-яё])(?:'
    r'бог(?:а|у|ом|е|и|ов|ам|ами|ах|иня|ини|ине|иню)?(?![а-яё])|бож(?:еств|ий|ья(?! коровк)|ье|ьи|ниц)|богородиц|богомол|богосл|аллах|всевышн|господ(?:ь|а|у|ом|е)?(?![а-яё])|господн|'
    r'жрец|жреч|молит|молен|молельщ|молеб|молельн|моления|пророк|пророч|коран|ислам|мусульман|мечет|минарет|шариат|паломн|библи|евангел|апостол|мессия|иисус|христ|'
    r'синагог|фарисе|дьякон|диакон|епископ|архиепископ|пастор|лютеран|католи|православ|протестант|литург|псал|проповед|ерес|еретик|апокалипс|праведн|архангел|'
    r'церк|ангел|дьявол|сатан|шайтан|джинн|демон|нечисть|нечист(?:ая|ой|ую) сил|злой дух|бес(?:а|ы|ов|ам)?(?![а-яё])|чёрт|черт(?:и|ей|ов)?(?![а-яё])|'
    r'ад(?:а|у|ом)?(?![а-яё])|ра(?:й|я|ю|ем)(?![а-яё])|загробн|судный|воскрес(?:ени|л)|греш|грех|свят|священ|причащ|причаст|рождеств|икон|душ(?:а|и|у|ой|е)(?![а-яё])|'
    r'крест(?!ьян|ов[кн]|оцвет|ц|ец|ообраз)|креще|крестин|жертвопринош|жертвовател|религ|вероучен|верующ|вероотступ|вера(?![а-яё])|веры(?![а-яё])|язычес|язычник|культ(?:а|ов|у|ом|е|овый|овое|овая)?(?![а-яё])|'
    r'храм|монах|монаш|монастыр|мулл|имам|поп(?:а|у|ом|ы|ов)?(?![а-яё])|пасх|троиц|идол|шаман|колдов|колдун|ведьм|знахар|гадал|гадани|маги(?:я|и|ю|ей|ческ)|заклинан|чародей|волшеб|'
    r'похорон|покойн|кладбищ|могил(?!ьник)|саван|поминк|мертвец|усопш|гроб(?!ов)|'
    r'пост(?:ить|иться)|разговлен|благослов|проклят|проклина|милостын|ниспослан|обет(?:а|ы)?(?![а-яё])|чудотвор|чудо(?![а-яё])|поклоня|поклонени|гада(?:ть|ю|ние)|предсказ|заговарив|призрак|привидени|предопредел|предначерт|(?<![а-яё])рок(?![а-яё])|обряд|ритуал|'
    r'миф(?![а-яё])|мистич|мистик|будди|буддиз|будда|индуи|кришн|лама(?:изм|истск)|кикимор|нежит|водяно|леши|гном|эльф|тролл|леший|домовой|русалк|дракон|вампир|оборот|фея|феи(?![а-яё])|мифол|гороскоп|астрол'
    r')', re.I)

# profanity / adult / drugs / alcohol / violence (Russian clue roots and Wiktionary labels) + Finnish roots
BAD_RU = re.compile(r'(?<![а-яё])(?:хуй|хуе|хуё|пизд|ебат|ебан|ёб|бляд|блят|сука|суки|жоп|говн|дерьм|срат|ссат|мудак|мудил|пидор|педик|шлюх|гандон|залуп|'
                    r'дурак|дура(?![а-яё])|идиот|урод|дебил|кретин|негр(?!амот)|жид|нацист|фашист|наркот|героин|убий|убить|убива|труп|смерт|умер|секс|порн|эрот|'
                    r'член(?: тела)?(?= мужск)|половой|половые|половых|испражн|кал(?![а-яё])|навоз|моча|мочи|мочиться|задниц|ягодиц|анус|задний проход|'
                    r'блуд|разврат|распут|проститут|любовни|изнасил|водк|самогон|пьян|алкогол|спиртн|вино(?![а-яё])|винн|пив(?:о|а)(?![а-яё])|окурок|сигарет|табак|опьян|самоубий|казн(?:ь|ить|и(?![а-яё]))|виселиц|палач|'
                    r'насил|гибел|погиб|умира|калеч|увеч|голый|обнаж|пивовар|снотвор|огнестрел|'
                    r'penis|vagina|vulgar|offensive|derogatory|feces|faeces|urine|sexual)', re.I)
BAD_LABELS = ('бран.', 'груб.', 'вульг.', 'неценз.', 'презр.', 'обсц.', 'мат.', 'религ.', 'мифол.', 'церк.', 'рел.', 'пренебр.', 'сексол.', 'астрол.', 'жарг.', 'slang')
BAD_FI = re.compile(r'^(?:paska|vittu|vitu|kusi|kuse|pillu|kyrp|mulkk|munn|perse|huor|horo|runkk|nussi|naid|neeker|ryyp|viina|viini|olut|olue|kalja|kalj|tupak|'
                    r'kuol|tappa|raisk|alasto|menehty|turma|silpo|mystin|mystiik|panimo|unilääk|tuliase|tapo|murha|itsemurh|homo|lesbo|hintti|ämmä|äpär|idioot|tyhm|ääli|pask)')

def religious(w, clue=''):
    w = w.lower()
    if w in STOP_WORDS or STOP_RE.match(w): return True
    return bool(clue and GLOSS_RE.search(clue.lower()))

def offensive(w, clue='', labels=''):
    if BAD_FI.match(w.lower()): return True
    if labels and any(l in labels for l in BAD_LABELS): return True
    return bool(clue and BAD_RU.search(clue.lower()))
