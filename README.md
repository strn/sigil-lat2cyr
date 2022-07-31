# sigil-lat2cyr

Додатак програму [Сигил](https://sigil-ebook.com/) за пресловљавање текста у [ЕПУБ](https://en.wikipedia.org/wiki/EPUB) датотекама са хрватске латинице на српску ћирилицу.

## Инсталација

Програмски додатак `sigil-lat2cyr` захтева присуство Питон модула `lxml` на рачунару корисника.

### Модул lxml

Најједноставнија инсталација овог модула јесте путем механизма `pip`. Потребно је отворити командни прозор оперативног система и задати следећу команду:

    python3 -m pip install lxml

### Програмски додатак sigil-lat2cyr

- Преузети најновију верзију датотеке [одавде](https://github.com/strn/sigil-lat2cyr/releases/latest)
- Отворити програм Сигил
- Из главног менија `Plugins` изабрати опцију `Manage Plugins`
- Кликнути на дугме `Add Plugin`
- Помоћу прозора за избор датотека наћи претходно преузету датотеку `lat2cyr.zip`
- Кликнути на дугме `Select` односно `Open`
- Додатак ће се појавити у листи програмских додатака (plugin)
- По жељи прећи на језичак `Shortcuts`
- У једном од слободних падајућих менија изабрати `lat2cyr`
- Кликнути на дугме `Ok`

На овај начин програмски додатак биће директно доступан кликом на дугме за директан позив програмског додатка. То дугме корисник ће познати по икони великог ћириличног слова `Ћ` на белој позадини.

## Коришћење

Програмски додатак `sigil-lat2cyr` може се позвати на један од следећих начина:

- Избором из главног менија `Plugins`, затим `Edit` па `lat2cyr`
- Кликом на дугме са великим ћириличним словом `Ћ` на белој позадини.

У оба случаја појавиће се прозор у којем ће бити исписани резултати корака пресловљавања. Кликом на дугме `Start` почиње процес пресловљавања. Кликом на дугме `Cancel` додатак неће бити покренут, а корисник ће бити враћен на главни прозор.


## Проблеми и предлози

Уколико корисник наиђе на проблем у раду програмског додатка или има предлог за његово побољшање, потребно је да:
- оде на везу [Issues](https://github.com/strn/sigil-lat2cyr/issues)
- Кликне на зелено дугме са натписом `New Issue`
- Укратко опише проблем или предложи измену
- Кликне на зелено дугме `Submit new issue`

Проблем тј. предлог биће узети у поступак у складу са расположивим временом аутора програма.
