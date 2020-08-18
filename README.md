# Kia Uvo

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][maintenance-homepage]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Lokalise][lokalise-shield]][lokalise]


# Work in Progress: Currently only works in Canada


_Component to integrate with [kia uvo][kia_uvo]._

Allows the user to see the last known state of the door sensors, locks and has a entity containing all the data returned from kia, It also exposes services to lock/unlock the vehicle

**This component will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.

![kia_uvo][kiauvoimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `kia_uvo`.
4. Download _all_ the files from the `custom_components/kia_uvo/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Kia Uvo"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/kia_uvo/translations/en.json
custom_components/kia_uvo/__init__.py
custom_components/kia_uvo/binary_sensor.py
custom_components/kia_uvo/config_flow.py
custom_components/kia_uvo/const.py
custom_components/kia_uvo/manifest.json
custom_components/kia_uvo/strings.json
custom_components/kia_uvo/services.yaml
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[kia_uvo]: https://github.com/wcomartin/kia_uvo
[maintenance-homepage]: http://williamcomartin.com
[buymecoffee]: https://www.buymeacoffee.com/wcomartin
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/wcomartin/kia_uvo.svg?style=for-the-badge
[commits]: https://github.com/wcomartin/kia_uvo/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[kiauvoimg]: https://upload.wikimedia.org/wikipedia/en/0/0d/Kia_UVO_Logo.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/wcomartin/kia_uvo.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-William%20Comartin-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/wcomartin/kia_uvo.svg?style=for-the-badge
[releases]: https://github.com/wcomartin/kia_uvo/releases
[lokalise]: https://app.lokalise.com/project/952864945eb373f8910863.60939812
[lokalise-shield]: https://img.shields.io/badge/Lokalise-Kia%20Uvo-green.svg?style=for-the-badge
