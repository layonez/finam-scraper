// run code in console on finam.ru
const instruments = aEmitentIds.map((id, i) => ({
  id,
  name: aEmitentNames[i],
  code: aEmitentCodes[i],
  market: aEmitentMarkets[i],
  decp: aEmitentDecp[id],
  url: aEmitentUrls[id],
  child: aEmitentChild[i],
}));
const markets = Finam.IssuerProfile.Main.markets.sort(
  (a, b) => a.value - b.value
);

// save to instruments
JSON.stringify(instruments);
// save to classes
JSON.stringify(markets);
