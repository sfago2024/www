function displayAdAndLogPageview() {
  const ads = [
    // {name: 'sfago2024-placeholder', extension: 'png', url: 'https://www.sfago2024.org/advertise-exhibit/#maury-a-castro'},
    {name: 'barenreiter', extension: 'jpg', url: 'https://www.barenreiter.us/products/bach-the-complete-organ-works-barenreiter?_pos=1&_psq=Bach+Organ+Works&_ss=e&_v=1.0'},
    {name: 'mader-fund', extension: 'jpg', url: 'https://www.maderscholarshipfund.org/'},
    {name: 'yale-ism', extension: 'jpg', url: 'https://ism.yale.edu/'},
  ];
  let ad = ads[Math.floor(Math.random() * ads.length)];
  document.querySelectorAll('.ad.desktop img').forEach((img) => { img.src = `/a/${ad.name}-desktop.${ad.extension}`; });
  document.querySelectorAll('.ad.mobile img').forEach((img) => { img.src = `/a/${ad.name}-mobile.${ad.extension}`; });
  document.querySelectorAll('.ad a').forEach((a) => {
    a.href = ad.url;
    if (ad.name != 'sfago2024-placeholder') {
      a.rel = 'external';
      a.target = '_blank';
    }
  });
  document.querySelectorAll('.ad').forEach((ad) => { ad.style.visibility = "visible"; });

  plausible('pageview', {props: {ad_displayed: ad.name}});
}

document.addEventListener('DOMContentLoaded', displayAdAndLogPageview);
