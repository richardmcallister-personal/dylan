# Hand-written song genealogies for site/data/lives/. Plain, factual, own words. Never quote lyrics.
# Each life: d (YYYY, YYYY-MM or YYYY-MM-DD), kind, title, place, note, optional a (album slug), change.
# kind: Roots · Written · Demo · Studio · Outtake · Live · Film · Broadcast
# change: "New arrangement" / "New words" / "Both" when the version changed the song.
# Setlist ids are filled in by tools/build_lives.py from the setlist data when a show on that date exists.
SONGS = {
"blowin-in-the-wind": {
  "intro": "Written in a few hours in April 1962 and sung at Gerde's Folk City the same month, before he had even finished it to his liking. Within a year it was an anthem — first in other people's voices.",
  "lives": [
    {"d": "1962", "kind": "Roots", "title": "An old spiritual underneath", "place": "Greenwich Village", "note": "The tune draws on \"No More Auction Block\", a spiritual sung by people escaping slavery. His own Gaslight Cafe performance of it from 1962 later came out on The Bootleg Series Vol. 1–3.", "a": "the-bootleg-series-vol-1-3-rare-and-unreleased-1961-1991"},
    {"d": "1962-04-16", "kind": "Live", "title": "First time out", "place": "Gerde's Folk City, New York", "note": "The earliest performance on record, in an early form of the song."},
    {"d": "1962-07-09", "kind": "Studio", "title": "The Freewheelin' recording", "place": "Columbia Studio A, New York", "note": "Just voice, guitar and harmonica. Released in May 1963 as the opening track of The Freewheelin' Bob Dylan.", "a": "freewheelin-bob-dylan"},
    {"d": "1963-06", "kind": "Cover", "title": "Peter, Paul and Mary", "place": "Single", "note": "Their harmony version reached number two in the US in summer 1963 and made the song known well beyond the folk clubs."},
    {"d": "1963-07-26", "kind": "Live", "title": "Newport finale", "place": "Newport Folk Festival", "note": "The festival closed with Dylan, Joan Baez, Peter, Paul and Mary, Pete Seeger and the Freedom Singers singing it together, arm in arm."},
    {"d": "1978-02-28", "kind": "Live", "title": "Slow and gospel-tinged", "place": "Nippon Budokan, Tokyo", "note": "Re-arranged for the 1978 big band with backing singers, slowed down and almost hymn-like. On Bob Dylan at Budokan.", "a": "bob-dylan-at-budokan", "change": "New arrangement"},
    {"d": "1985-07-13", "kind": "Live", "title": "Live Aid", "place": "JFK Stadium, Philadelphia", "note": "The last song of his short acoustic set with Keith Richards and Ronnie Wood, seen around the world."},
    {"d": "2012", "kind": "Live", "title": "The late encore", "place": "Never Ending Tour", "note": "From 2012 to 2019 it was a regular encore, rearranged several times and often led from the piano.", "change": "New arrangement"}
  ],
  "others": [
    {"who": "Peter, Paul and Mary", "y": 1963, "note": "Number two in the US."},
    {"who": "Stevie Wonder", "y": 1966, "note": "A soul version that went top ten in the US."},
    {"who": "Sam Cooke", "y": 1964, "note": "Didn't record a hit version, but said the song spurred him to write \"A Change Is Gonna Come\"."}
  ]
},
"mr-tambourine-man": {
  "intro": "Begun after a trip to Mardi Gras in New Orleans in February 1964 and finished that spring. Dylan sang it for a year before releasing it — by which time the Byrds were about to turn it into a number one.",
  "lives": [
    {"d": "1964-05-17", "kind": "Live", "title": "First performance", "place": "Royal Festival Hall, London", "note": "Probably the live debut, months before any recording was released."},
    {"d": "1964-06-09", "kind": "Outtake", "title": "With Ramblin' Jack Elliott", "place": "Columbia Studio A, New York", "note": "Tried during the Another Side sessions with Elliott singing harmony. Left off the album, it surfaced in 2005 on No Direction Home.", "a": "bootleg-series-vol-7-no-direction-home"},
    {"d": "1964-07-26", "kind": "Live", "title": "Newport 1964", "place": "Newport Folk Festival", "note": "Sung solo at the festival a year before the electric set; the crowd was hearing it for the first time."},
    {"d": "1965-01-15", "kind": "Studio", "title": "The master take", "place": "Columbia Studio A, New York", "note": "Acoustic guitar and harmonica with Bruce Langhorne's electric guitar weaving around them. On Bringing It All Back Home, March 1965.", "a": "bringing-it-all-back-home"},
    {"d": "1965-04-12", "kind": "Cover", "title": "The Byrds", "place": "Single", "note": "One of his four verses, a jangling twelve-string guitar and close harmonies. Number one in the US and UK, and often called the start of folk rock.", "change": "Both"},
    {"d": "1966-05-17", "kind": "Live", "title": "End of the acoustic half", "place": "Free Trade Hall, Manchester", "note": "On the 1966 world tour it closed the solo acoustic set every night, stretched out with long harmonica passages. On The Bootleg Series Vol. 4.", "a": "bootleg-series-vol-4-bob-dylan-live-1966"},
    {"d": "1978-02-28", "kind": "Live", "title": "With flute", "place": "Nippon Budokan, Tokyo", "note": "The 1978 band gave it a gentle arrangement with flute. On Bob Dylan at Budokan.", "a": "bob-dylan-at-budokan", "change": "New arrangement"}
  ],
  "others": [
    {"who": "The Byrds", "y": 1965, "note": "Number one on both sides of the Atlantic."},
    {"who": "Judy Collins", "y": 1965, "note": "An early folk cover on her Fifth Album."}
  ]
},
"tangled-up-in-blue": {
  "intro": "The opening song of Blood on the Tracks and the one he has rewritten most openly. The story jumps between people, places and times, and Dylan has kept moving its pieces around for fifty years.",
  "lives": [
    {"d": "1974-09", "kind": "Studio", "title": "The New York version", "place": "A&R Studios, New York", "note": "Recorded quietly with a small band, and pressed on the first test copies of the album. Released in 1991 on The Bootleg Series Vol. 1–3, and the full session on More Blood, More Tracks.", "a": "more-blood-more-tracks-the-bootleg-series-vol-14"},
    {"d": "1974-12-30", "kind": "Studio", "title": "Re-cut in Minneapolis", "place": "Sound 80, Minneapolis", "note": "Just before release he re-recorded it with local musicians his brother found, faster and brighter. This is the version on Blood on the Tracks, January 1975.", "a": "blood-tracks", "change": "New arrangement"},
    {"d": "1975-11-13", "kind": "Live", "title": "Rolling Thunder", "place": "Rolling Thunder Revue", "note": "Played in the acoustic part of the 1975 shows. Recordings from the tour came out in 2019.", "a": "bob-dylan-the-rolling-thunder-revue-the-1975-live-recordings"},
    {"d": "1984-07-07", "kind": "Live", "title": "Heavily revised", "place": "Wembley Stadium, London", "note": "Solo acoustic with many lines rewritten — some verses close to new. Dylan said he preferred the imagery. Released on Real Live.", "a": "real-live", "change": "New words"},
    {"d": "1998", "kind": "Live", "title": "Never Ending Tour fixture", "place": "Never Ending Tour", "note": "In the late 1990s it was in nearly every show, usually acoustic with a long guitar coda, more than 100 times a year from 1998 to 2000."},
    {"d": "2010", "kind": "Live", "title": "Still changing", "place": "Never Ending Tour", "note": "In the 2010s the words kept shifting from tour to tour, with whole verses reworked again.", "change": "New words"}
  ],
  "others": [
    {"who": "Jerry Garcia Band", "note": "A long-running part of Garcia's live sets."}
  ]
},
"all-along-the-watchtower": {
  "intro": "A short, spare song from John Wesley Harding that Jimi Hendrix turned into something huge. Dylan has said that when he plays it now, he is following Hendrix's lead. It is his most-played song on stage.",
  "lives": [
    {"d": "1967-11-06", "kind": "Studio", "title": "Three men in Nashville", "place": "Columbia Studio A, Nashville", "note": "Dylan on guitar and harmonica with Charlie McCoy on bass and Kenny Buttrey on drums. Under three minutes. On John Wesley Harding, December 1967.", "a": "john-wesley-harding"},
    {"d": "1968-01", "kind": "Cover", "title": "Jimi Hendrix", "place": "Olympic Studios, London", "note": "Recorded within weeks of Dylan's album coming out, layered with electric guitar solos. On Electric Ladyland; the single went top five in the UK.", "change": "New arrangement"},
    {"d": "1974-01", "kind": "Live", "title": "First on stage", "place": "The 1974 tour with the Band", "note": "Played loud and fast with the Band, now built on Hendrix's model. On Before the Flood. The 1974 shows are not in this site's concert data yet.", "a": "before-the-flood", "change": "New arrangement"},
    {"d": "1978-02-28", "kind": "Live", "title": "Big band", "place": "Nippon Budokan, Tokyo", "note": "Part of the 1978 big-band show with horns and backing singers. On Bob Dylan at Budokan.", "a": "bob-dylan-at-budokan"},
    {"d": "1992", "kind": "Live", "title": "The closer", "place": "Never Ending Tour", "note": "From the early 1990s it became a fixture near the end of the show, often the final song, for more than twenty years."}
  ],
  "others": [
    {"who": "Jimi Hendrix Experience", "y": 1968, "note": "UK top five; the version most people know."},
    {"who": "U2", "y": 1988, "note": "A live version on Rattle and Hum."},
    {"who": "Neil Young", "y": 1992, "note": "At the 30th anniversary concert in Madison Square Garden."}
  ]
},
"knockin-on-heavens-door": {
  "intro": "Written for a death scene in Sam Peckinpah's western Pat Garrett and Billy the Kid, in which Dylan also acted. Two short verses that turned into one of his most recorded songs.",
  "lives": [
    {"d": "1973-02", "kind": "Film", "title": "For the film", "place": "Burbank Studios, California", "note": "Recorded for the soundtrack to play under the death of a sheriff. Released on Pat Garrett & Billy the Kid in July 1973; the single reached number 12 in the US.", "a": "pat-garrett-and-billy-the-kid"},
    {"d": "1974-01", "kind": "Live", "title": "On tour with the Band", "place": "The 1974 tour with the Band", "note": "Added to the 1974 shows. The 1974 shows are not in this site's concert data yet.", "a": "the-1974-live-recordings"},
    {"d": "1975", "kind": "Live", "title": "Rolling Thunder", "place": "Rolling Thunder Revue", "note": "Part of the 1975 Rolling Thunder shows, sung with the whole troupe behind him.", "a": "bob-dylan-the-rolling-thunder-revue-the-1975-live-recordings"},
    {"d": "1978-03-01", "kind": "Live", "title": "Reggae", "place": "Nippon Budokan, Tokyo", "note": "Recast with a reggae lilt by the 1978 band. On Bob Dylan at Budokan.", "a": "bob-dylan-at-budokan", "change": "New arrangement"}
  ],
  "others": [
    {"who": "Eric Clapton", "y": 1975, "note": "A reggae-flavoured single."},
    {"who": "Guns N' Roses", "y": 1991, "note": "On Use Your Illusion II; a number two single in the UK."}
  ]
},
"visions-of-johanna": {
  "intro": "One of the songs he wrote in late 1965, between the electric tours. He tried it first as a band song, then found the slow, drifting version in Nashville.",
  "lives": [
    {"d": "1965-11-30", "kind": "Outtake", "title": "\"Freeze Out\" with the Hawks", "place": "Columbia Studio A, New York", "note": "Cut fast and edgy with the band he was touring with, under the working title Freeze Out. Released on No Direction Home and The Cutting Edge.", "a": "bootleg-series-vol-7-no-direction-home"},
    {"d": "1966-02-14", "kind": "Studio", "title": "The Nashville master", "place": "Columbia Studio A, Nashville", "note": "Slowed right down with Nashville session players and Al Kooper's organ. On Blonde on Blonde, June 1966.", "a": "blonde-on-blonde", "change": "New arrangement"},
    {"d": "1966-05-17", "kind": "Live", "title": "Solo in 1966", "place": "Free Trade Hall, Manchester", "note": "Played alone with guitar and harmonica in the hushed first half of the 1966 shows. On The Bootleg Series Vol. 4.", "a": "bootleg-series-vol-4-bob-dylan-live-1966"},
    {"d": "2012", "kind": "Live", "title": "Late revival", "place": "Never Ending Tour", "note": "Rarely played for decades, it came back often in 2012 and 2013."}
  ],
  "others": [
    {"who": "Grateful Dead", "y": 1986, "note": "Took it into their own live sets from 1986."}
  ]
},
"girl-from-the-north-country": {
  "intro": "Written after his first trip to England in the winter of 1962–63. The melody and some of the shape come from the English folk song \"Scarborough Fair\", which he learned from Martin Carthy in London.",
  "lives": [
    {"d": "1962-12", "kind": "Roots", "title": "Learning from Martin Carthy", "place": "London", "note": "Carthy taught him his arrangement of Scarborough Fair; Dylan built a new song on its frame."},
    {"d": "1963-04-23", "kind": "Studio", "title": "Freewheelin'", "place": "Columbia Studio A, New York", "note": "Voice, finger-picked guitar and harmonica. On The Freewheelin' Bob Dylan.", "a": "freewheelin-bob-dylan"},
    {"d": "1969-02-18", "kind": "Studio", "title": "Duet with Johnny Cash", "place": "Columbia Studio A, Nashville", "note": "Sung together in Nashville and used to open Nashville Skyline, Dylan in his new, smoother voice.", "a": "nashville-skyline", "change": "New arrangement"},
    {"d": "2019", "kind": "Live", "title": "Back in the set", "place": "Never Ending Tour", "note": "Played in most shows of 2019, Dylan at the piano."}
  ],
  "others": [
    {"who": "Conor McPherson", "y": 2017, "note": "A stage musical named after the song, built on Dylan's catalogue, opened at the Old Vic and went on to Broadway."}
  ]
},
"simple-twist-of-fate": {
  "intro": "A song from the New York sessions for Blood on the Tracks that survived the re-recording in Minneapolis, so the album keeps its first, quiet version.",
  "lives": [
    {"d": "1974-09", "kind": "Studio", "title": "New York take", "place": "A&R Studios, New York", "note": "Acoustic guitar, bass and harmonica. This take stayed on Blood on the Tracks; the full session is on More Blood, More Tracks.", "a": "blood-tracks"},
    {"d": "1975-09-10", "kind": "Broadcast", "title": "First performance, on TV", "place": "WTTW studio, Chicago", "note": "Played for a television tribute to John Hammond, the producer who signed him — the first time it was performed live."},
    {"d": "1978-02-28", "kind": "Live", "title": "Big band", "place": "Nippon Budokan, Tokyo", "note": "Given the full 1978 band treatment. On Bob Dylan at Budokan.", "a": "bob-dylan-at-budokan", "change": "New arrangement"},
    {"d": "2018", "kind": "Live", "title": "Back in nearly every show", "place": "Never Ending Tour", "note": "After years as an occasional song it was played almost nightly in 2018 and 2019."}
  ],
  "others": [
    {"who": "Joan Baez", "y": 1975, "note": "On Diamonds & Rust, the same year as Dylan's album."}
  ]
},
"masters-of-war": {
  "intro": "A protest song written in winter 1962–63, set to an old tune. He has kept it in the set for six decades, often in arrangements that sound nothing like the original.",
  "lives": [
    {"d": "1962", "kind": "Roots", "title": "Nottamun Town", "place": "Kentucky tradition", "note": "The melody comes from \"Nottamun Town\" as arranged by the Kentucky folk singer Jean Ritchie. His lawyers later settled with her."},
    {"d": "1963-04-24", "kind": "Studio", "title": "Freewheelin'", "place": "Columbia Studio A, New York", "note": "Voice and guitar, harsh and steady. On The Freewheelin' Bob Dylan.", "a": "freewheelin-bob-dylan"},
    {"d": "1963-04-12", "kind": "Live", "title": "Town Hall", "place": "Town Hall, New York", "note": "One of the early concert performances, at his first major New York hall show."},
    {"d": "1991-02-20", "kind": "Broadcast", "title": "The Grammys, during the Gulf War", "place": "Radio City Music Hall, New York", "note": "Accepting a lifetime achievement award, he played it fast and loud with a band, the words hard to make out — a choice many saw as a comment on the war.", "change": "New arrangement"}
  ],
  "others": [
    {"who": "Eddie Vedder and Mike McCready", "y": 1992, "note": "At the 30th anniversary concert in Madison Square Garden."}
  ]
},
"dont-think-twice-its-all-right": {
  "intro": "A farewell song from 1962, built on a tune he picked up from his friend Paul Clayton. It has stayed in the set, in one form or another, through almost every era.",
  "lives": [
    {"d": "1962", "kind": "Roots", "title": "Borrowed bones", "place": "Greenwich Village", "note": "The melody and some phrasing come from \"Who's Gonna Buy You Ribbons When I'm Gone\", which Paul Clayton had adapted from an older song."},
    {"d": "1962-11-14", "kind": "Studio", "title": "Freewheelin'", "place": "Columbia Studio A, New York", "note": "Fast finger-picked guitar and harmonica. On The Freewheelin' Bob Dylan.", "a": "freewheelin-bob-dylan"},
    {"d": "1963", "kind": "Cover", "title": "Peter, Paul and Mary", "place": "Single", "note": "A top ten hit in the US in 1963, following their Blowin' in the Wind."},
    {"d": "1978-02-28", "kind": "Live", "title": "Reggae", "place": "Nippon Budokan, Tokyo", "note": "Turned into a reggae song for the 1978 tour. On Bob Dylan at Budokan.", "a": "bob-dylan-at-budokan", "change": "New arrangement"}
  ],
  "others": [
    {"who": "Peter, Paul and Mary", "y": 1963, "note": "US top ten."},
    {"who": "Johnny Cash", "y": 1965, "note": "On Orange Blossom Special."}
  ]
},
"i-shall-be-released": {
  "intro": "Written in the Basement Tapes summer of 1967, when Dylan and the Band were making music for fun in a house near Woodstock. The Band's version came first; Dylan's own studio take waited until 1971.",
  "lives": [
    {"d": "1967", "kind": "Demo", "title": "The basement", "place": "Big Pink, West Saugerties", "note": "Recorded with the Band on a home tape machine. The take first came out officially in 1991, and in full on The Basement Tapes Complete.", "a": "bootleg-series-vol-11-basement-tapes-complete"},
    {"d": "1968-07", "kind": "Cover", "title": "The Band", "place": "Music from Big Pink", "note": "Closed their first album, with Richard Manuel singing high and fragile."},
    {"d": "1971-09", "kind": "Studio", "title": "Dylan's own release", "place": "New York", "note": "A new recording with Happy Traum on second guitar, made for Bob Dylan's Greatest Hits Vol. II.", "a": "bob-dylans-greatest-hits-volume-ii"},
    {"d": "1976-11-25", "kind": "Live", "title": "The Last Waltz", "place": "Winterland, San Francisco", "note": "The Band's farewell concert ended with everyone on stage singing it together."},
    {"d": "2026-06-09", "kind": "Live", "title": "Back after 18 years", "place": "Cuthbert Amphitheater, Eugene", "note": "Played for the first time since June 2008, as the last song of the night, and kept in the set through 2026."}
  ],
  "others": [
    {"who": "The Band", "y": 1968, "note": "On Music from Big Pink."},
    {"who": "Nina Simone", "y": 1969, "note": "On To Love Somebody."}
  ]
},
"make-you-feel-my-love": {
  "intro": "A plain love song from Time Out of Mind that other singers took up almost at once. Billy Joel released it before Dylan's own album came out.",
  "lives": [
    {"d": "1997-01", "kind": "Studio", "title": "Time Out of Mind", "place": "Criteria Studios, Miami", "note": "Recorded with Daniel Lanois producing, Dylan on piano. On Time Out of Mind, September 1997.", "a": "time-out-of-mind"},
    {"d": "1997-08", "kind": "Cover", "title": "Billy Joel goes first", "place": "Greatest Hits Volume III", "note": "Released as \"To Make You Feel My Love\" a month before Dylan's album."},
    {"d": "1997-11-02", "kind": "Live", "title": "First performance", "place": "Never Ending Tour", "note": "Added to the shows within weeks of the album."},
    {"d": "1998", "kind": "Cover", "title": "Garth Brooks", "place": "Hope Floats soundtrack", "note": "A number one on the US country chart."},
    {"d": "2008", "kind": "Cover", "title": "Adele", "place": "19", "note": "Her piano version became a UK top five hit in 2010."}
  ],
  "others": [
    {"who": "Billy Joel", "y": 1997, "note": "First to release it."},
    {"who": "Garth Brooks", "y": 1998, "note": "US country number one."},
    {"who": "Adele", "y": 2008, "note": "UK number four in 2010."}
  ]
},
"every-grain-of-sand": {
  "intro": "The closing song of Shot of Love, from the end of his gospel years. Forty years later it became the last song of every show.",
  "lives": [
    {"d": "1980-09", "kind": "Demo", "title": "Demo with a barking dog", "place": "Rundown Studios, Santa Monica", "note": "A rough demo with piano and a dog barking in the background. Released on The Bootleg Series Vol. 1–3.", "a": "the-bootleg-series-vol-1-3-rare-and-unreleased-1961-1991"},
    {"d": "1981", "kind": "Studio", "title": "Shot of Love", "place": "Clover Studios, Los Angeles", "note": "Closes the album, with harmonica and backing vocals.", "a": "shot-love"},
    {"d": "1981-11-21", "kind": "Live", "title": "First performance", "place": "Lakeland Civic Center, Florida", "note": "Played on the last nights of the 1981 tour."},
    {"d": "2021-11", "kind": "Live", "title": "The closing song", "place": "Rough and Rowdy Ways tour", "note": "Since the tour began in November 2021 it has ended nearly every show, Dylan at the piano, with a harmonica solo.", "change": "New arrangement"}
  ],
  "others": [
    {"who": "Emmylou Harris", "y": 1995, "note": "On Wrecking Ball."}
  ]
},
"desolation-row": {
  "intro": "The eleven-minute closer of Highway 61 Revisited, a long parade of characters from history and fiction. The only acoustic song on an electric album.",
  "lives": [
    {"d": "1965-07-29", "kind": "Outtake", "title": "Electric first", "place": "Columbia Studio A, New York", "note": "Tried with a band first. The electric take came out on The Cutting Edge.", "a": "the-bootleg-series-vol-12-the-best-of-the-cutting-edge-1965-1966"},
    {"d": "1965-08-04", "kind": "Studio", "title": "Acoustic master", "place": "Columbia Studio A, New York", "note": "Re-cut acoustic with Charlie McCoy's Spanish-flavoured guitar fills. Closes Highway 61 Revisited.", "a": "highway-61-revisited", "change": "New arrangement"},
    {"d": "1965-08-28", "kind": "Live", "title": "First performance", "place": "Forest Hills Tennis Stadium, New York", "note": "Played in the solo acoustic half of the show, two days before the album came out."},
    {"d": "1994-11-18", "kind": "Live", "title": "Unplugged", "place": "Sony Music Studios, New York", "note": "Played with a small acoustic band for MTV, released on MTV Unplugged.", "a": "mtv-unplugged"},
    {"d": "2017", "kind": "Live", "title": "Nightly again", "place": "Never Ending Tour", "note": "Back in almost every show of 2017, and again on the 2025 tour."}
  ],
  "others": [
    {"who": "My Morning Jacket", "y": 2009, "note": "For the film Watchmen."}
  ]
}
}
