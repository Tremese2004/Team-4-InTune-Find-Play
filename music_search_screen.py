
import 'lyric_search_page.dart';
import 'package:flutter/material.dart';

// This is the starting point of the InTune application.
void main() {
  runApp(const InTuneApp());
}

// This class creates the main application.
class InTuneApp extends StatelessWidget {
  const InTuneApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // Removes the debug banner from the top corner.
      debugShowCheckedModeBanner: false,

      // Sets the application name.
      title: 'InTune',

      // Sets the overall app theme and background colour.
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF171323),
        useMaterial3: true,
      ),

      // Opens the Music Search screen when the app starts.
      home: const MusicSearchScreen(),
    );
  }
}

// This class creates the Music Search screen.
// StatefulWidget allows the screen to update when the user interacts with it.
class MusicSearchScreen extends StatefulWidget {
  const MusicSearchScreen({super.key});

  @override
  State<MusicSearchScreen> createState() =>
      _MusicSearchScreenState();
}

// This class stores the information and actions for the Music Search screen.
class _MusicSearchScreenState extends State<MusicSearchScreen> {

  // Controls and stores the text entered into the search bar.
  final TextEditingController searchController =
      TextEditingController();

  // These variables store the colours used throughout the app.
  final Color background = const Color(0xFF171323);
  final Color purple = const Color(0xFFB69AFF);
  final Color pink = const Color(0xFFEA91D8);
  final Color cardBackground = const Color(0xFF292238);

  // Stores the message displayed after a search.
  String searchMessage = '';

  // Stores the song and artist shown in the mini-player.
  String currentSong = 'Blinding Lights';
  String currentArtist = 'The Weeknd';

  // Tracks whether the mini-player is playing or paused.
  bool isPlaying = false;

  // Lets us open favorites from library.
  bool showingFavorites = false;

  // Keeps track of which bottom navigation tab is selected.
  // 0 = Home, 1 = Library, 2 = Search, 3 = Playlist.
  int selectedTab = 2;
  int previousTab = 2;


  void goBack() {
    setState(() {
      selectedTab = previousTab;
      showingFavorites = false;
    });
  }

  final Set<String> followedArtists = {};

  //Add or remove a song from Favorites
  void toggleFavorite(Map<String, String> song) {
    setState(() {
      final exists = favoriteSongs.any(
        (item) => item['title'] == song['title'],
      );

      if (exists) {
        favoriteSongs.removeWhere(
          (item) => item['title'] == song['title'],
        );
      } else {
        favoriteSongs.add(
          Map<String, String>.from(song),
        );
      }
    });
  }

  //Check whether a song is a favorite
  bool isFavorite(Map<String, String> song) {
    return favoriteSongs.any(
      (item) => item['title'] == song['title'],
    );
  }

  //Favorite screen
  Widget buildFavoriteScreen() {
    return StatefulBuilder(
      builder: (context, updateFavorites) {
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Padding(
              padding: EdgeInsets.all(20),
              child: Text(
                'Favorites',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),

            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: TextField(
                decoration: InputDecoration(
                  hintText: 'Search favorites..',
                  prefixIcon: const Icon(Icons.search),
                  filled: true,
                  fillColor: cardBackground,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                    borderSide: BorderSide.none,
                  ),
                ),
                onChanged: (value) {
                  updateFavorites(() {});
                },
              ),
            ),

            const SizedBox(height: 15),

            Expanded(
              child: favoriteSongs.isEmpty
                  ? const Center(
                    child: Text('You have no favorite songs yet.'),
                  )
                : ListView.builder(
                  itemCount: favoriteSongs.length,
                  itemBuilder: (context, index) {
                    final song = favoriteSongs[index];

                    return ListTile(
                      leading: Icon(
                        Icons.music_note,
                        color: pink,
                      ),

                      title: Text(song['title'] ?? ''),
                      subtitle: Text(song['artist'] ?? ''),

                      onTap: () => playLibrarySong(song),

                      trailing: IconButton(
                        icon: const Icon(
                          Icons.favorite,
                          color: Colors.pink,
                        ),
                        onPressed: () {
                          toggleFavorite(song);
                          updateFavorites(() {});
                        },
                      ),
                    );
                  },
                ),
            ),
          ],
        );
      },
    );
  }

  Map<String, String>? selectedArtistSong;

  //Opens Artist Information for the selected song
  void openArtistInformation(Map<String, String> song) {
    setState(() {
      selectedArtistSong = song;
    });

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: background,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, updateArtist) {
            final artist = song['artist'] ?? 'Unknown Artist';
            final isFollowed = followedArtists.contains(artist);

            return SizedBox(
              height: 600,
              child: Padding(
                padding: const EdgeInsets.all(22),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: Container(
                        width: 45,
                        height: 5,
                        decoration: BoxDecoration(
                          color: Colors.white38,
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                    ),

                    const SizedBox(height: 25),

                    const Icon(
                      Icons.person,
                      size: 75,
                      color: Colors.white70,
                    ),

                    const SizedBox(height: 15),

                    Text(
                      artist,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 27,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 15),

                    Row(
                      children: [
                        Expanded(
                          child: ElevatedButton(
                            onPressed: () {
                              playLibrarySong(song);
                              Navigator.pop(context);
                            },
                            child: const Text('Play Music'),
                          ),
                        ),

                        const SizedBox(width: 10),

                        Expanded(
                          child: OutlinedButton(
                            onPressed: () {
                              setState(() {
                                if (isFollowed) {
                                  followedArtists.remove(artist);
                                } else {
                                  followedArtists.add(artist);
                                }
                              });

                              updateArtist(() {});
                            },
                            child: Text(
                              'Related Songs',
                              style: TextStyle(
                                fontSize: 21,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ),

                        const SizedBox(height: 10),

                        ListTile(
                          leading: Icon(
                              Icons.music_note,
                              color: pink,
                            ),
                            title: Text(
                              song['title'] ?? ''
                            ),
                            subtitle: Text(artist),
                            onTap: () {
                              playLibrarySong(song);
                              Navigator.pop(context);
                            },
                          ),
                          
                          const SizedBox(height: 15),
                          
                          const Text(
                            'About the Artists',
                            style: TextStyle(
                              fontSize: 21,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          
                          const SizedBox(height: 8),
                            Text(
                              'Explore music by $artist. '
                              'Discover songs and keep track of your favorite artists.',
                                style: const TextStyle(
                                  color: Colors.white70,
                                ),
                            ),
                          ]),
                        ],
                      ),
                    ),
                  );
                },
              );
            },
          );
        }

  //Sample song catalog
  final List<Map<String, String>> songCatalog = [
    {'title': 'SET IT OFF', 'artist': 'Offset', 'duration': '3.02'},
    {'title': 'Under the Sun', 'artist': 'Dreamville, J. Cole, DaBaby, Lute', 'duration': '3.59'},
    {'title': 'Bodies', 'artist': 'Offset & JID', 'duration': '3.25'},
    {'title': 'Surround Sound', 'artist': 'JID, 21 Savage, Baby Tate', 'duration': '3.49'},
    {'title': 'Like That', 'artist': 'Future, Metro Boomin', 'duration': '4.27'},
    {'title': 'BUTTERFLY EFFECT', 'artist': 'Travis Scott', 'duration': '3.11'},
    {'title': 'heart pt.6', 'artist': 'Kendrick Lamar', 'duration': '4.10'},
    {'title': 'Do for love', 'artist': '2Pac', 'duration': '4.46'},
    {'title': 'meet the grahams', 'artist': 'Kendrick Lamar', 'duration': '6.06'},
    {'title': "Can't Tell Me Nothing ", 'artist': 'Kanye West', 'duration': '4.31'},
    {'title': 'Have You Ever', 'artist': 'Brandy', 'duration': '4.05'},
  ];

  //Library and listening activity
  final List<Map<String, String >> librarySongs = [];
  final List<Map<String, String >> favoriteSongs = [];
  final List<Map<String, String >> recentSaves = [];
  final List<Map<String, String >> recentPlays = [];

  //Initial playlists
  final Map<String, List<Map<String, String>>> playlists = {
    'Shower Jamz': [],
    'Gym Set': [],
    'Work Mix': [],
  };

  String activePlaylist = 'Shower Jamz';

  @override
  void initState() {
    super.initState();

    playlists['Shower Jamz'] = songCatalog
        .map((song) => Map<String, String>.from(song))
        .toList();
    
    playlists['Gym Set'] = [
      songCatalog[4],
      songCatalog[5],
      songCatalog[0]
    ].map((song) => Map<String, String>.from(song)).toList();

    playlists['Work Mix'] = [
      songCatalog[6],
      songCatalog[8],
      songCatalog[10]
    ].map((song) => Map<String, String>.from(song)).toList();
  }

  // This list stores the information for all nine music genres.
  // Each genre has a name, background colour, image, and height.
  final List<Map<String, dynamic>> genres = [
    {
      'name': 'Hip Hop',
      'color': const Color(0xFF55DCE0),
      'image': 'assets/images/hiphop.png',
      'height': 160.0,
    },
    {
      'name': 'R&B',
      'color': const Color(0xFFFF555B),
      'image': 'assets/images/rnb.png',
      'height': 190.0,

      //imaging positioning and size
      'imageAlignment': Alignment.bottomRight,
      'imageScale': 2.1,
    },
    {
      'name': 'Pop',
      'color': const Color(0xFFFF914D),
      'image': 'assets/images/pop.png',
      'height': 240.0,
    },
    {
      'name': 'Jazz',
      'color': const Color(0xFF78D957),
      'image': 'assets/images/jazz.png',
      'height': 85.0,

      //imaging positioning and size
      'imageAlignment': Alignment.topLeft,
      'imageScale': 1.35,
    },
    {
      'name': 'Rock',
      'color': const Color(0xFFB8FF70),
      'image': 'assets/images/rock.png',
      'height': 85.0,
    },
    {
      'name': 'Afro Beats',
      'color': const Color(0xFFFF3038),
      'image': 'assets/images/afro.png',
      'height': 200.0,

      //imaging positioning and size
      'imageAlignment': Alignment.bottomLeft,
      'imageScale': 1.0,
    },
    {
      'name': 'Hits',
      'color': const Color(0xFFFF59BB),
      'image': 'assets/images/hits.png',
      'height': 235.0,

      //imaging positioning and size
      'imageAlignment': Alignment.bottomCenter,
      'imageScale': 1.7,
    },
    {
      'name': 'Country',
      'color': const Color(0xFF997500),
      'image': 'assets/images/country.png',
      'height': 130.0,
    },
    {
      'name': 'Blues',
      'color': const Color(0xFF0753B5),
      'image': 'assets/images/blues.png',
      'height': 180.0,
    },
  ];

  // This function runs when the user presses the Search button.
  void searchMusic() {
    // Gets the text entered by the user and removes extra spaces.
    final query = searchController.text.trim();

    // setState updates the screen when information changes.
    setState(() {
      // Checks whether the search bar is empty.
      if (query.isEmpty) {
        searchMessage = 'Please enter a song or artist.';
      } else {
        // Displays the search term entered by the user.
        // This is a demonstration, not a real music search.
        searchMessage =
            'You searched for "$query". Connect a music service to find real results.';
      }
    });
  }

  // This function runs when the user taps a genre card.
  void selectGenre(String genre) {
    setState(() {
      // Places the selected genre into the search bar.
      searchController.text = genre;

      // Clears the previous search message.
      searchMessage = '';
    });
  }

  // This function clears the search bar when the X is pressed.
  void clearSearch() {
    setState(() {
      searchController.clear();
      searchMessage = '';
    });
  }

  // This function switches the mini-player between playing and paused.
  void togglePlay() {
    setState(() {
      // Changes the playing status to its opposite.
      isPlaying = !isPlaying;
    });
  }

  // This function changes the song displayed in the mini-player.
  void nextSong() {
    setState(() {
      currentSong = 'Next Song';
      currentArtist = 'Artist Name';

      // The new placeholder song starts in the paused state.
      isPlaying = false;
    });
  }

  // This function updates the selected bottom navigation tab.
  void selectNavigation(int index) {
    setState(() {
      if (selectedTab  != index) {
        previousTab = selectedTab;
      }

      selectedTab = index;
      showingFavorites = false;
    });
  }

  //Plays songs and updates recent plays
  void playLibrarySong(Map<String, String> song) {
    setState(() {
      currentSong = song['title'] ?? 'Unknown Song';
      currentArtist = song['artist'] ?? 'Unknown Artist';

      // The new placeholder song starts in the paused state.
      isPlaying = true;

      recentPlays.removeWhere(
        (item) => item['title'] == song['title'],
      );

      recentPlays.insert(
        0,
        Map<String, String>.from(song),
      );

      if (recentPlays.length > 10) {
        recentPlays.removeLast();
      }
    });
  }

  //Saves a song to the library and recent saves
  void saveSong(Map<String, String> song) {
    setState(() {
      if (!librarySongs.any(
        (item) => item['title'] == song['title'],
      )) {
        librarySongs.add(Map<String, String>.from(song));
      }

      recentSaves.removeWhere(
        (item) => item['title'] == song['title'],
      );

      recentSaves.insert(
        0,
        Map<String, String>.from(song),
      );

      if (recentSaves.length > 10) {
        recentSaves.removeLast();
      }
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Saved ${song['title']} to your library'),
      ),
    );
  }

  //Creates a new playlist
  void createPlaylist() {
    final controller = TextEditingController();

    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        backgroundColor: cardBackground,
        title: const Text('Create Playlist'),
        content: TextField(
          controller: controller,
          autofocus: true,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            hintText: 'Playlist name',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () {
              final name = controller.text.trim();

              if (name.isNotEmpty &&
                  !playlists.containsKey(name)) {
                setState(() {
                  playlists[name] = [];
                });

                Navigator.pop(dialogContext);

                setState(() {
                  selectedTab = 3;
                });
                }
            },
            child: const Text('Create'),
          ),
        ],
      ),
    );
  }

  //Opens Library screen
  Widget buildLibraryScreen() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Your Library',
            style: TextStyle(
              fontSize: 28,
              color: Colors.white,
            ),
          ),

          const SizedBox(height: 8),

          Text(
            'Your music, all in one place',
            style: TextStyle(color: Colors.white70),
          ),

          const SizedBox(height: 25),

          // Library shortcuts 
          Row(
            children: [
              Expanded(
                child: libraryCard(
                  'Recent Saves',
                  recentSaves.length,
                  Icons.bookmark,
                  () => showSongCollection(
                    'Recent Saves',
                    recentSaves,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: libraryCard(
                  'Recent Plays',
                  recentPlays.length,
                  Icons.history,
                  () => showSongCollection(
                    'Recent Plays',
                    recentPlays,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 12),

          Row(
            children: [
              Expanded(
                child: libraryCard(
                  'Favorites',
                  favoriteSongs.length,
                  Icons.favorite,
                  () => showSongCollection(
                    'Favorites',
                    favoriteSongs,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: libraryCard(
                  'Saved Songs',
                  librarySongs.length,
                  Icons.library_music,
                  () => showSongCollection(
                    'Saved Songs',
                    librarySongs,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 30),


          //Playlist Header
          Row(
            mainAxisAlignment:MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'My Playlists',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),

              IconButton(
                onPressed: createPlaylist,
                icon: Icon(
                  Icons.add_circle,
                  color: purple,
                  size: 30,
                ),
              ),
            ],
          ),

          const SizedBox(height: 10),

          ...playlists.keys.map((name) {
            return ListTile(
              contentPadding: EdgeInsets.zero,
              leading: CircleAvatar(
                backgroundColor: cardBackground,
                child: Icon(
                  Icons.queue_music,
                  color: pink,
                ),
              ),
              title: Text(name),
              subtitle: Text(
                '${playlists[name]!.length} songs'
              ),
              trailing: const Icon(
                Icons.arrow_forward_ios,
                size: 16,
              ),
              onTap: () {
                setState(() {
                  activePlaylist = name;
                  selectedTab = 3;
                });
              },
            );
          }),
        ],
      ),
    );
  }

  //Reusable Library Card
  Widget libraryCard(
    String title,
    int count,
    IconData icon,
    VoidCallback onTap,
  ) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: cardBackground,
          borderRadius: BorderRadius.circular(15),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: purple, size: 27),
            const SizedBox (height: 12),
            Text(
              title,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 5),
            Text(
              '$count songs',
              style: const TextStyle(
                fontSize: 12,
                color: Colors.white70,
              ),
            ),
          ]
        )
      ),
    );
  }

  //Displays a selected song collection.
  void showSongCollection(
    String title,
    List<Map<String, String>> songs,
  ) {
    // Implementation for displaying the song collection goes here.
    showModalBottomSheet(
      context: context,
      backgroundColor: background,
      builder: (context) {
        return SizedBox(
          height: 450,
          child: Column (
            children: [

              Padding(
                padding: const EdgeInsets.all(18),
                child: Row(
                  children: [
                    //return to the previous screen
                    IconButton(
                      icon:const Icon(
                        Icons.arrow_back,
                        color: Colors.white,
                      ),
                      onPressed: () {
                        Navigator.pop(context);
                      },
                    ),

                    const SizedBox(width: 10),

                    Expanded(
                      child: Text(
                        title,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 22,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              Expanded(
                child: songs.isEmpty
                    ? const Center(
                        child: Text('No songs yet.'),
                      )
                      : ListView.builder(
                          itemCount: songs.length,
                          itemBuilder:(context, index) {
                            final song = songs[index];
                            
                            return songTile(song);
                          },
                        ),
              ),
            ],
          ),
        );
      },
    );
  }

  //Reusable song row
  Widget songTile(Map<String, String> song) {
    return ListTile(
      leading: CircleAvatar(
        backgroundColor: cardBackground,
        child: Icon(
          Icons.music_note,
          color: pink,
        ),
      ),

      title: Text(song['title'] ?? ''),
      subtitle: Text(song['artist'] ?? ''),

      trailing: PopupMenuButton<String>(
        onSelected: (action) {
          if (action == 'play') {
            playLibrarySong(song);
          } else if (action == 'Save') {
            saveSong(song);
          } else if (action == 'Favorite') {
            toggleFavorite(song);
          }
        },
        itemBuilder:(context) => const [
          PopupMenuItem(
            value: 'Play',
            child: Text('Play'),
          ),
          PopupMenuItem(
            value: 'Save',
            child: Text('Save to Library'),
          ),
          PopupMenuItem(
            value: 'Favorite',
            child: Text('Add to Favorites'),
          )
        ],
      ),

      onTap: () => playLibrarySong(song),
    );
  }

  //Playlist Screen
  Widget buildPlaylistScreen() {
    final songs = playlists[activePlaylist] ?? [];

    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Playlist content goes here
          Row(
            children: [
              const Expanded(
                child: Text(
                  'My Playlist',
                  style: TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),

              IconButton(
                onPressed: renamePlaylist,
                icon: Icon(Icons.add, color: pink),
              ),
            ],
          ),

          const SizedBox(height: 15),

          Text(
            activePlaylist,
            style: TextStyle(
              fontSize: 21,
              color: purple,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 6),

          Text(
            '${songs.length} tracks',
            style: const TextStyle(
              color: Colors.white70,
            ),
          ),

          const SizedBox(height: 20),

          Expanded(
            child: songs.isEmpty
                ? const Center(
                  child: Text('Add songs to this playlist'),
                )
              : ListView.builder(
                itemCount: songs.length,
                itemBuilder:(context, index) {
                  final song = songs[index];

                  return ListTile(
                    leading: Icon(
                      Icons.music_note,
                      color: pink,
                    ),

                    title: Text(song['title'] ?? ''),
                    subtitle: Text(song['artist'] ?? ''),

                    onTap: () => playLibrarySong(song),

                    trailing: IconButton(
                      icon: const Icon(
                        Icons.remove_circle_outline,
                        color: Colors.redAccent,
                      ),
                      onPressed: () {
                        setState(() {
                          songs.removeAt(index);
                        });
                      }
                    ),
                  );
                },
              ),

          ),
        ],
      ),
    );
  }

  // Renames the current playlist.
  void renamePlaylist() {
    final controller = TextEditingController(
      text: activePlaylist,
    );

    showDialog<String>(
      context: context,
      builder: (dialogcontext) => AlertDialog(
        title: const Text('Rename Playlist'),

        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            hintText: 'New playlist name',
          ),
        ),

        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogcontext),
            child: const Text('Cancel'),
          ),

          ElevatedButton(
            onPressed: () {
              final newName = controller.text.trim();

              if (newName.isNotEmpty &&
                 !playlists.containsKey(newName)) {
                setState(() {
                  playlists[newName] =
                      playlists.remove(activePlaylist)!;
                  activePlaylist = newName;
                });

                Navigator.pop(dialogcontext);
              }
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  //Add songs to the current playlist.
  void addSongsToPlaylists() {
    showModalBottomSheet(
      context: context,
      backgroundColor: background,
      isScrollControlled: true,

      builder: (context) {
        return SizedBox(
          height: 500,
          child: Column(
            children: [
              const Padding(
                padding: EdgeInsets.all(18),
                child: Text(
                  'Add Songs',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),

              Expanded(
                child: ListView.builder(
                  itemCount: songCatalog.length,

                  itemBuilder: (context, index) {
                    final song = songCatalog[index];

                    return ListTile(
                      title: Text(song['title']!),
                      subtitle: Text(song['artist']!),

                      trailing: IconButton(
                        icon: Icon(
                          Icons.add_circle,
                          color: purple,
                        ),

                        onPressed: () {
                          setState(() {
                            final playlist =
                                playlists[activePlaylist]!;
                            
                            if (!playlist.any(
                              (item) =>
                                  item['title'] == song['title'],
                            )) {
                              playlist.add(
                                Map<String, String>.from(song),
                              );
                            }
                          });
                        },
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
  

  // Disposes of the search controller when the screen is removed.
  // This helps prevent unnecessary memory use.
  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  Widget buildSelectedScreen() {
    if (showingFavorites) {
      return Column(
        children: [
          ListTile(
            leading: IconButton(
              icon: const Icon(Icons.arrow_back),
              onPressed: () {
                setState(() {
                  showingFavorites = false;
                });
              },
            ),
            title: const Text('Favorites'),
          ),
          Expanded(
            child: buildFavoriteScreen(),
          ),
        ],
      );
    }

    switch (selectedTab) {
      case 0:
        return buildHomeScreen();
      
      case 1:
        return buildLibraryScreen();
      
      case 2:
        return buildSearchScreen();
      
      case 3:
        return buildPlaylistScreen();
      
      case 4:
        return LyricSearchPage(
          onBack: goBack,
        );
      
      default:
        return buildSearchScreen();
    }
  }

  Widget buildHomeScreen() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(22),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 15),

          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Good Morning,',
                    style: TextStyle(
                      color: Colors.grey,
                      fontSize: 14,
                    ),
                  ),
                  Text(
                    'User',
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
              IconButton(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Profile coming soon!'),
                    ),
                  );
                },
                icon: const Icon(
                  Icons.account_circle,
                  size: 32,
                ),
              ),
            ],
          ),

          const SizedBox(height: 28),

          TextField(
            controller: searchController,
            onSubmitted: (_) {
              setState(() {
                selectedTab = 2;
                showingFavorites = false;
              });
              searchMusic();
            },
            decoration: InputDecoration(
              hintText: 'Search by lyrics, song, or artist...',
              prefixIcon: const Icon(Icons.search),
              suffixIcon: IconButton(
                icon: const Icon(Icons.arrow_forward),
                onPressed: () {
                  setState(() {
                    selectedTab = 2;
                    showingFavorites = false;
                  });
                  searchMusic();
                },
              ),
              filled: true,
              fillColor: cardBackground,
              border:OutlineInputBorder(
                borderRadius: BorderRadius.circular(14),
                borderSide: BorderSide.none,
              ),
            ),
          ),

          const SizedBox(height: 25),

          Container(
            decoration:BoxDecoration(
              gradient: const LinearGradient(
                colors: [
                  Color(0xFFAB42F5),
                  Color(0xFF5936F5),
                ],
              ),
              borderRadius: BorderRadius.circular(16),
            ),
            child: ListTile(
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Voice Search is coming soon!'),
                  ),
                );
              },
              leading: const Icon(
                Icons.mic,
                size: 32,
                color: Colors.white,
              ),
              title: const Text(
                'Voice Search',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: const Text('Hum or sing a song'),
              trailing: const Icon(Icons.arrow_forward),
            ),
          ),

          const SizedBox(height: 15),

          Container(
            decoration:BoxDecoration(
              gradient: const LinearGradient(
                colors: [
                  Color(0xFF2196F3),
                  Color(0xFF007BFF),
                ],
              ),
              borderRadius: BorderRadius.circular(16),
            ),
            child: ListTile(
              onTap:() {
                setState(() {
                  selectedTab = 4;
                  showingFavorites = false;
                });
              },
              leading: const Icon(
                Icons.keyboard,
                size: 32,
                color: Colors.white,
              ),
              title: const Text(
                'Type Lyrics',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: const Text('Know some of the words of the song?'),
              trailing: const Icon(Icons.arrow_forward),
            ),
          ),

          const SizedBox(height: 35),

          const Text(
            'Quick Access',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),

          const SizedBox(height: 20),

          Row(
            children: [
              homeQuickButton(
                Icons.library_music,
                'Your Playlist',
                () => selectNavigation(3),
              ),
              homeQuickButton(
                Icons.favorite,
                'Favorites',
                () {
                  setState(() {
                    selectedTab = 1;
                    showingFavorites = true;
                  });
                },
              ),
              homeQuickButton(
                Icons.history,
                'Search History',
                () => selectNavigation(1),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget homeQuickButton(
    IconData icon,
    String title,
    VoidCallback onTap,
  ) {
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Column(
          children: [
            CircleAvatar(
              radius: 25,
              backgroundColor: cardBackground,
              child: Icon(icon, color: Colors.white),
            ),
            const SizedBox(height: 8),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildSearchScreen() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(22),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Search screen content goes here.
          SingleChildScrollView(
                // Adds spacing around the screen content.
                padding: const EdgeInsets.all(22),

                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [

                    // HEADER
                    // Displays the InTune logo and profile icon.
                    Row(
                      mainAxisAlignment:
                          MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            // Music equalizer icon.
                            Icon(
                              Icons.graphic_eq,
                              color: purple,
                              size: 42,
                            ),

                            const SizedBox(width: 10),

                            // InTune application name.
                            Text(
                              'InTune',
                              style: TextStyle(
                                color: purple,
                                fontSize: 34,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),

                        // Profile icon on the right side of the header.
                        IconButton(
                          onPressed: () {
                            ScaffoldMessenger.of(context)
                                .showSnackBar(
                              const SnackBar(
                                content: Text(
                                  'Profile screen coming soon!',
                                ),
                              ),
                            );
                          },
                          icon: const Icon(
                            Icons.account_circle_outlined,
                            size: 34,
                            color: Colors.white,
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 34),

                    // PAGE TITLE
                    // Introduces the Music Search screen.
                    const Text(
                      'Search Music',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 12),

                    // Short description underneath the page title.
                    const Text(
                      'Find your favorite songs, artists, and genres.',
                      style: TextStyle(
                        color: Color(0xFFB8B3C9),
                        fontSize: 16,
                      ),
                    ),

                    const SizedBox(height: 28),

                    // SEARCH FIELD
                    // Allows users to type a song or artist name.
                    TextField(
                      controller: searchController,

                      // Sets the colour and size of the typed text.
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 17,
                      ),

                      // Allows users to search by pressing Enter.
                      onSubmitted: (_) => searchMusic(),

                      decoration: InputDecoration(
                        // Text displayed before the user types.
                        hintText: 'Search songs or artists...',
                        hintStyle: const TextStyle(
                          color: Color(0xFFB8B3C9),
                        ),

                        // Search icon on the left side of the field.
                        prefixIcon: Icon(
                          Icons.search,
                          color: purple,
                          size: 29,
                        ),

                        // X button on the right clears the search.
                        suffixIcon: IconButton(
                          onPressed: clearSearch,
                          icon: const Icon(
                            Icons.close,
                            color: Color(0xFFB8B3C9),
                          ),
                        ),

                        // Gives the search field its dark background.
                        filled: true,
                        fillColor: cardBackground,

                        // Border shown when the search field is not selected.
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(25),
                          borderSide: BorderSide(
                            color: purple.withValues(alpha: 0.5),
                            width: 1.5,
                          ),
                        ),

                        // Border shown when the user selects the search field.
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(25),
                          borderSide: BorderSide(
                            color: purple,
                            width: 2,
                          ),
                        ),

                        // Adds space inside the search field.
                        contentPadding:
                            const EdgeInsets.symmetric(
                          vertical: 21,
                          horizontal: 18,
                        ),
                      ),
                    ),

                    const SizedBox(height: 16),

                    // SEARCH BUTTON
                    // Runs the searchMusic function when tapped.
                    SizedBox(
                      width: double.infinity,
                      height: 53,
                      child: ElevatedButton.icon(
                        onPressed: searchMusic,

                        // Search icon displayed inside the button.
                        icon: const Icon(
                          Icons.search,
                          color: Color(0xFF171323),
                        ),

                        // Text displayed inside the button.
                        label: const Text(
                          'Search',
                          style: TextStyle(
                            color: Color(0xFF171323),
                            fontSize: 17,
                          ),
                        ),

                        // Styles the button with the pink colour and rounded edges.
                        style: ElevatedButton.styleFrom(
                          backgroundColor: pink,
                          shape: RoundedRectangleBorder(
                            borderRadius:
                              BorderRadius.circular(30),
                          ),
                        ),
                      ),
                    ),

                    // SEARCH MESSAGE
                    // Only appears when a search message exists.
                    if (searchMessage.isNotEmpty) ...[
                      const SizedBox(height: 16),

                      Text(
                        searchMessage,
                        style: const TextStyle(
                          color: Color(0xFFB8B3C9),
                          fontSize: 15,
                        ),
                      ),
                    ],

                    const SizedBox(height: 38),

                    // GENRE SECTION TITLE
                    const Text(
                      'Browse Genres',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 20),

                    // GENRE CARDS
                    // This Row creates two cloumns of genre cards.
                    // Each colummn contains cards with different heights.
                    // creates the staggered layout shwin in the Canva design.
                    // GridView.builder creates all nine genre cards.

                    Row(
                      //Aligns both columns at the top
                      crossAxisAlignment: CrossAxisAlignment.start,

                      children: [

                        // LEFT COLUMN
                        // Expanded gives the left column half of the available width.
                        Expanded( 
                          child: Column(
                            children: [

                              //Displays the hiphop card
                              genreCard(genres[0]),

                              const SizedBox(height: 10),

                              //Displays the pop card
                              genreCard(genres[2]),

                              const SizedBox(height: 10),

                              //Displays the rock card
                              genreCard(genres[4]),

                              const SizedBox(height: 10),

                              //Displays the hits card
                              genreCard(genres[6]),
                            ],
                          ),
                        ),
                        // Adds apace between the two columns
                        const SizedBox(width: 10),

                        // RIGHT COLUMN
                        // Expanded gives the right column the remaining width.
                        Expanded(
                          child: Column(
                            children: [

                              //Displays the rnb card
                              genreCard(genres[1]),
                              
                              const SizedBox(height: 10),

                              //Displays the jazz card
                              genreCard(genres[3]),

                              const SizedBox(height: 10),

                              //Displays the afrobeat card
                              genreCard(genres[5]),

                              const SizedBox(height: 10),

                              //Displays the country card
                              genreCard(genres[7]),

                              const SizedBox(height: 10),

                              //Displays the blues card
                              genreCard(genres[8]),
                          ],
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      );
   }


  // This method builds everything displayed on the Music Search screen.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: background,

      // SafeArea keeps content away from the phone's status bar
      // and other system areas.
      body: SafeArea(
        child: Column(
          children: [

            //shows back arrows when opening secondary screen
            if (selectedTab == 4)
              Align(
                alignment: Alignment.centerLeft,
                child: IconButton(
                  icon: const Icon(
                    Icons.arrow_back,
                    color: Colors.white,
                  ),
                  onPressed: goBack,
                  tooltip: 'Back',
                ),
              ),

            // MAIN SCREEN changes based on the selected tab.
            // Expanded allows this section to use the available space.
            Expanded(
              child: buildSelectedScreen(),
            ),


            // MINI-PLAYER
            // Displays the current song and playback controls.
            Container(
              color: cardBackground,

              // Adds spacing inside the mini-player.
              padding: const EdgeInsets.symmetric(
                horizontal: 18,
                vertical: 13,
              ),

              child: Row(
                children: [

                  // Placeholder album artwork.
                  Container(
                    height: 65,
                    width: 65,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [purple, pink],
                      ),
                      borderRadius: BorderRadius.circular(16),
                    ),

                    child: const Icon(
                      Icons.music_note,
                      color: Color(0xFF171323),
                      size: 37,
                    ),
                  ),

                  const SizedBox(width: 13),

                  // Displays the song title and artist.
                  Expanded(
                    child: Column(
                      crossAxisAlignment:
                          CrossAxisAlignment.start,
                      children: [
                        Text(
                          currentSong,
                          style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),

                        const SizedBox(height: 4),

                        Text(
                          currentArtist,
                          style: const TextStyle(
                            color: Color(0xFFB8B3C9),
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Play or pause button.
                  IconButton(
                    onPressed: togglePlay,
                    icon: Icon(
                      isPlaying
                          ? Icons.pause
                          : Icons.play_arrow,
                      color: purple,
                      size: 31,
                    ),
                  ),

                  // Next song button.
                  IconButton(
                    onPressed: nextSong,
                    icon: Icon(
                      Icons.skip_next,
                      color: pink,
                      size: 31,
                    ),
                  ),
                ],
              ),
            ),

            // BOTTOM NAVIGATION BAR
            // Allows users to select different app sections.
            Container(
              color: const Color(0xFF211C31),

              padding: const EdgeInsets.symmetric(
                vertical: 9,
                horizontal: 5,
              ),

              child: Row(
                mainAxisAlignment:
                    MainAxisAlignment.spaceAround,
                children: [

                  // Home navigation button.
                  navigationItem(
                    Icons.home_outlined,
                    'Home',
                    0,
                  ),

                  // Library navigation button.
                  navigationItem(
                    Icons.library_music_outlined,
                    'Library',
                    1,
                  ),

                  // Search navigation button.
                  navigationItem(
                    Icons.search,
                    'Search',
                    2,
                  ),

                  // Playlist navigation button.
                  navigationItem(
                    Icons.queue_music,
                    'Playlist',
                    3,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // This reusable function creates an individual genre card.
  // It displayed a coloured background, an artist image and a genre name.
  Widget genreCard(Map<String, dynamic> genre) {
    
    // GestureDetector allows the user to tap the genre cards.
    return GestureDetector(
      
      // When tapped, the selected genre is placed in the search bar.
      onTap: () => selectGenre(genre['name']),

      child: Container(
        
        // Sets the card height using the genre list
        height: genre['height'],

        //makes the card fill the available column width
        width: double.infinity,

        // Sets the cards background colour and rounded corners.
        decoration: BoxDecoration(
          color: genre['color'],
          borderRadius: BorderRadius.circular(5),
        ),

        //keeps the image inside the cards boundaries
        clipBehavior: Clip.antiAlias,

        //stack allows the image and genre name to overlap
        child: Stack(
          children: [

            //positions the artist image across the card
            Positioned.fill(
              child: Transform.scale(
                //Enlarge or reduce each genre image individually
                scale: genre['imageScale'] ?? 1.0,

                alignment:
                  genre['imageAlignment'] ?? Alignment.bottomCenter,
                  
                child: Image.asset( 
                //loads the image using its file path
                genre['image'],

                //fits the image inside the card without cropping it
                fit: BoxFit.contain,

                alignment:
                  genre['imageAlignment'] ?? Alignment.bottomCenter,

                //display a music from icon if the image cannot load
                errorBuilder: (context, error, stackTrace) {
                  return const Center(
                    child: Icon(
                      Icons.music_note,
                      size: 45,
                      color: Colors.black54,
                    ),
                  );
                },
              ),
            ),
          ),
            
            //positions the genre name in the top-left corner
            Positioned(
              top: 7,
              left: 7,
              
              //displays the genre name
              child: Text(
                genre['name'],
                
                //styles the genre name
                style: const TextStyle(
                  color: Colors.black,
                  fontSize: 17,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }


  // This function creates each bottom navigation item.
  // It highlights the selected tab and handles user taps.
  Widget navigationItem(
    IconData icon,
    String label,
    int index,
    ) {
      
      // Checks whether this navigation item is selected.
      final bool selected = selectedTab == index;
      
      return GestureDetector(
        // Updates the selected tab when tapped.
        onTap: () => selectNavigation(index),
        
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Creates the rounded background behind the icon.
            Container(
              padding: const EdgeInsets.symmetric(
                horizontal: 22,
                vertical: 7,
              ),
              
              decoration: BoxDecoration(
                color: selected
                  ? const Color(0xFF493B67)
                  : Colors.transparent,
                borderRadius: BorderRadius.circular(30),
              ),
              
              // Displays the navigation icon.
              child: Icon(
                icon,
                color: selected
                ? Colors.white
                : const Color(0xFFB8B3C9),
              size: 27,
            ),
          ),
          
          const SizedBox(height: 4),
          
          // Displays the navigation label. 
          Text(
            label,
            style: TextStyle(
              color: selected
                ? Colors.white
                : const Color(0xFFB8B3C9),
              fontSize: 13,
            ),
          ),
        ],
      ),
    );
  }
}
