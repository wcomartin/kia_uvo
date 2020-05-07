[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][maintenance-homepage]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Component to integrate with [kia uvo][kia_uvo]._

Allows the user to see the last known state of the door sensors, locks and has a entity containing all the data returned from kia, It also exposes services to lock/unlock the vehicle

**This component will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.

![kia_uvo][kiauvoimg]

{% if not installed %}
## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Kia Uvo".

{% endif %}


## Configuration is done in the UI

<!---->

***

[kia_uvo]: https://github.com/wcomartin/kia_uvo
[maintenance-homepage]: http://williamcomartin.com
[buymecoffee]: https://www.buymeacoffee.com/wcomartin
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/wcomartin/kia_uvo.svg?style=for-the-badge
[commits]: https://github.com/wcomartin/kia_uvo/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[kiauvoimg]: kia_uvo2.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/wcomartin/kia_uvo.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-William%20Comartin-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/wcomartin/kia_uvo.svg?style=for-the-badge
[releases]: https://github.com/wcomartin/kia_uvo/releases