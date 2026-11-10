import 'dart:math' as math;
import 'dart:ui' show ImageFilter;

import 'package:flutter/cupertino.dart' show CupertinoIcons;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';

import 'itunes.dart';

// iOS dark-mode colors and motion, shared across the app.
const Color surface = Color(0xFF1C1C1E);
const Color surfaceRaised = Color(0xFF2C2C2E);
const Color hairline = Color(0x1FFFFFFF); // white at 12%
const Color textPrimary = Colors.white;
const Color textSecondary = Color(0x99EBEBF5);
const Color textMuted = Color(0x8CEBEBF5);
const Color accent = Color(0xFFB69AFF);
const Color onAccent = Colors.black;
const Curve ease = Cubic(0.22, 1, 0.36, 1);

// A frosted glass surface, like the floating bars and buttons in iOS.
// Whatever is behind it shows through, blurred.
class Glass extends StatelessWidget {
  final double radius;
  final Widget child;

  const Glass({super.key, required this.radius, required this.child});

  @override
  Widget build(BuildContext context) {
    final shape = BorderRadius.circular(radius);

    return ClipRRect(
      borderRadius: shape,
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 24, sigmaY: 24),
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: const Color(0xA6242426),
            borderRadius: shape,
            border: Border.all(color: hairline),
          ),
          child: child,
        ),
      ),
    );
  }
}

// Song Detector (Voice Search), opened from the Voice Search card on Home.
// Note: recognition is simulated with a fixed demo result. Swap the
// listening timer for mic recording + a recognition API (e.g. ACRCloud, AudD)
// when the team picks one.
class SongDetectorPage extends StatefulWidget {
  final String currentSong; // song in the mini-player
  final bool isPlaying; // whether the mini-player is playing
  final void Function(Map<String, String> song) onPlay;
  final VoidCallback onTogglePlay;
  final double bottomInset; // space taken by the floating bars

  const SongDetectorPage({
    super.key,
    required this.currentSong,
    required this.isPlaying,
    required this.onPlay,
    required this.onTogglePlay,
    required this.bottomInset,
  });

  @override
  State<SongDetectorPage> createState() => _SongDetectorPageState();
}

class _SongDetectorPageState extends State<SongDetectorPage>
    with TickerProviderStateMixin {
  // The fixed result the demo "detects".
  static const Map<String, String> demoSong = {
    'title': 'Blinding Lights',
    'artist': 'The Weeknd',
  };

  // Rings that spread out from the button while listening.
  late final AnimationController rings = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 1800),
  );

  // Fills the ring around the button; when full, the song is "found".
  late final AnimationController listen = AnimationController(
    vsync: this,
    duration: const Duration(seconds: 3),
  )..addStatusListener((status) {
      if (status == AnimationStatus.completed) showResult();
    });

  // Plays the result entrance: sleeve, record, then text and buttons.
  late final AnimationController reveal = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 1100),
  );

  // Spins the record while this song is playing (one turn per 1.8s, 33 rpm).
  late final AnimationController spin = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 1800),
  );

  bool listening = false;
  bool found = false;
  bool pressed = false;
  String artwork = '';

  bool get playingThis =>
      widget.isPlaying && widget.currentSong == demoSong['title'];

  @override
  void initState() {
    super.initState();
    if (playingThis) spin.repeat();
  }

  @override
  void didUpdateWidget(SongDetectorPage oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (!playingThis) {
      spin.stop();
    } else if (!spin.isAnimating) {
      spin.repeat();
    }
  }

  void detect() {
    if (listening) return;
    HapticFeedback.mediumImpact();

    setState(() {
      listening = true;
      found = false;
    });

    rings.repeat();
    listen.forward(from: 0);
    loadArtwork();
  }

  void showResult() {
    HapticFeedback.heavyImpact();
    rings.stop();

    setState(() {
      listening = false;
      found = true;
    });

    reveal.forward(from: 0);
  }

  void detectAgain() {
    reveal.reset();
    listen.reset();
    detect();
  }

  // Loads the album cover while "listening", so it's ready for the reveal.
  Future<void> loadArtwork() async {
    if (artwork.isNotEmpty) return;
    try {
      final track = await findTrack(demoSong['title']!, demoSong['artist']!);
      if (mounted && track != null) setState(() => artwork = track.artworkUrl);
    } catch (_) {
      // No cover: the sleeve shows a plain music note instead.
    }
  }

  void playOrPause() {
    HapticFeedback.selectionClick();
    if (widget.currentSong == demoSong['title']) {
      widget.onTogglePlay();
    } else {
      widget.onPlay(demoSong);
    }
  }

  // Opens a Spotify or Apple Music search in the browser.
  void openService(String service) {
    final query =
        Uri.encodeComponent('${demoSong['title']} ${demoSong['artist']}');
    final url = service == 'spotify'
        ? 'https://open.spotify.com/search/$query'
        : 'https://music.apple.com/us/search?term=$query';
    launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
  }

  @override
  void dispose() {
    rings.dispose();
    listen.dispose();
    reveal.dispose();
    spin.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;

    return Stack(
      fit: StackFit.expand,
      children: [
        // Once a song is found, its cover fills the screen as a soft blur.
        AnimatedOpacity(
          opacity: found && artwork.isNotEmpty ? 1 : 0,
          duration: const Duration(milliseconds: 600),
          curve: ease,
          child: artwork.isEmpty
              ? const SizedBox.shrink()
              : ClipRect(
                  child: Stack(
                    fit: StackFit.expand,
                    children: [
                      ImageFiltered(
                        imageFilter: ImageFilter.blur(sigmaX: 60, sigmaY: 60),
                        child: Transform.scale(
                          scale: 1.4,
                          child: Image.network(
                            artwork,
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stack) =>
                                const SizedBox.shrink(),
                          ),
                        ),
                      ),
                      // Darkens the blur so white text stays readable.
                      const ColoredBox(color: Color(0x99000000)),
                    ],
                  ),
                ),
        ),
        Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.fromLTRB(24, top + 64, 24, widget.bottomInset),
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 300),
              switchInCurve: ease,
              switchOutCurve: ease,
              child: found ? buildResult() : buildDetector(),
            ),
          ),
        ),
      ],
    );
  }

  // ---------- Listening screen ----------

  Widget buildDetector() {
    return Column(
      key: const ValueKey('detector'),
      mainAxisSize: MainAxisSize.min,
      children: [
        const Text(
          "What's that song?",
          style: TextStyle(
            color: textPrimary,
            fontSize: 34,
            fontWeight: FontWeight.bold,
            letterSpacing: 0.4,
          ),
        ),
        const SizedBox(height: 8),
        const SizedBox(
          width: 300,
          child: Text(
            'Find it, then play it here or in Spotify or Apple Music',
            textAlign: TextAlign.center,
            style: TextStyle(color: textSecondary, fontSize: 17, height: 1.3),
          ),
        ),
        const SizedBox(height: 40),
        buildListenButton(),
        const SizedBox(height: 32),
        AnimatedSwitcher(
          duration: const Duration(milliseconds: 200),
          child: Text(
            listening ? 'Listening…' : 'Tap to listen',
            key: ValueKey(listening),
            style: const TextStyle(
              color: textPrimary,
              fontSize: 17,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
        const SizedBox(height: 40),
        const Text(
          'Demo mode: recognition is simulated,\nno microphone or account needed',
          textAlign: TextAlign.center,
          style: TextStyle(color: textSecondary, fontSize: 13, height: 1.4),
        ),
      ],
    );
  }

  // The big round button, with the progress ring and spreading rings.
  Widget buildListenButton() {
    return Semantics(
      button: true,
      label: listening ? 'Listening' : 'Listen for a song',
      child: GestureDetector(
        onTapDown: (_) => setState(() => pressed = true),
        onTapCancel: () => setState(() => pressed = false),
        onTapUp: (_) {
          setState(() => pressed = false);
          detect();
        },
        child: SizedBox(
          width: 240,
          height: 240,
          child: Stack(
            alignment: Alignment.center,
            children: [
              // Rings and progress, drawn behind the button.
              AnimatedBuilder(
                animation: Listenable.merge([rings, listen]),
                builder: (context, _) => CustomPaint(
                  size: const Size(240, 240),
                  painter: ListenRingsPainter(
                    spread: rings.value,
                    progress: listen.value,
                    active: listening,
                  ),
                ),
              ),
              AnimatedScale(
                scale: pressed ? 0.97 : 1,
                duration: const Duration(milliseconds: 120),
                curve: ease,
                child: Container(
                  width: 168,
                  height: 168,
                  decoration: const BoxDecoration(
                    color: accent,
                    shape: BoxShape.circle,
                  ),
                  alignment: Alignment.center,
                  child: AnimatedSwitcher(
                    duration: const Duration(milliseconds: 240),
                    switchInCurve: ease,
                    transitionBuilder: (child, animation) => FadeTransition(
                      opacity: animation,
                      child: ScaleTransition(
                        scale: Tween(begin: 0.85, end: 1.0).animate(animation),
                        child: child,
                      ),
                    ),
                    child: listening
                        ? const LiveBars(
                            key: ValueKey('bars'),
                            count: 5,
                            height: 44,
                            barWidth: 6,
                            color: onAccent,
                          )
                        : const Icon(
                            CupertinoIcons.mic_fill,
                            key: ValueKey('mic'),
                            size: 56,
                            color: onAccent,
                          ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // ---------- Result screen ----------

  Widget buildResult() {
    return Column(
      key: const ValueKey('result'),
      mainAxisSize: MainAxisSize.min,
      children: [
        rise(0, const Text(
          'Demo result',
          style: TextStyle(color: textSecondary, fontSize: 13),
        )),
        const SizedBox(height: 20),
        buildRecord(),
        const SizedBox(height: 28),
        rise(1, Text(
          demoSong['title']!,
          style: const TextStyle(
            color: textPrimary,
            fontSize: 28,
            fontWeight: FontWeight.bold,
            letterSpacing: 0.36,
          ),
        )),
        const SizedBox(height: 4),
        rise(2, Text(
          demoSong['artist']!,
          style: const TextStyle(color: textSecondary, fontSize: 20),
        )),
        const SizedBox(height: 28),
        rise(3, SizedBox(
          width: double.infinity,
          height: 50,
          child: FilledButton.icon(
            onPressed: playOrPause,
            style: FilledButton.styleFrom(
              backgroundColor: accent,
              foregroundColor: onAccent,
              shape: const StadiumBorder(),
            ),
            icon: Icon(
              playingThis ? CupertinoIcons.pause_fill : CupertinoIcons.play_fill,
              size: 18,
            ),
            label: Text(
              playingThis ? 'Pause' : 'Play preview',
              style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w600),
            ),
          ),
        )),
        const SizedBox(height: 12),
        rise(4, Row(
          children: [
            Expanded(child: serviceButton('Spotify', 'spotify')),
            const SizedBox(width: 12),
            Expanded(child: serviceButton('Apple Music', 'apple')),
          ],
        )),
        const SizedBox(height: 20),
        rise(5, TextButton.icon(
          onPressed: detectAgain,
          style: TextButton.styleFrom(foregroundColor: accent),
          icon: const Icon(CupertinoIcons.arrow_clockwise, size: 16),
          label: const Text('Detect again', style: TextStyle(fontSize: 17)),
        )),
      ],
    );
  }

  // Album sleeve with a record that slides out and spins while playing.
  Widget buildRecord() {
    const double sleeve = 220;
    const double disc = 208;

    return AnimatedBuilder(
      animation: reveal,
      builder: (context, _) {
        final sleeveIn = ease.transform((reveal.value / 0.45).clamp(0.0, 1.0));
        final discOut =
            ease.transform(((reveal.value - 0.3) / 0.5).clamp(0.0, 1.0));

        return Opacity(
          opacity: sleeveIn,
          child: Transform.translate(
            offset: Offset(0, (1 - sleeveIn) * 24),
            child: SizedBox(
              width: 300,
              height: sleeve,
              child: Stack(
                children: [
                  // The record starts hidden behind the sleeve, then slides right.
                  Positioned(
                    left: 6 + discOut * 80,
                    top: (sleeve - disc) / 2,
                    child: RotationTransition(
                      turns: spin,
                      child: Vinyl(size: disc, artwork: artwork),
                    ),
                  ),
                  Container(
                    width: sleeve,
                    height: sleeve,
                    decoration: BoxDecoration(
                      color: surface,
                      borderRadius: BorderRadius.circular(12),
                      boxShadow: const [
                        BoxShadow(
                          color: Color(0x73000000),
                          blurRadius: 24,
                          offset: Offset(0, 12),
                        ),
                      ],
                    ),
                    clipBehavior: Clip.antiAlias,
                    child: Cover(url: artwork, iconSize: 64),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget serviceButton(String label, String service) {
    return SizedBox(
      height: 50,
      child: FilledButton.icon(
        onPressed: () => openService(service),
        style: FilledButton.styleFrom(
          backgroundColor: const Color(0x29FFFFFF),
          foregroundColor: textPrimary,
          padding: const EdgeInsets.symmetric(horizontal: 12),
          shape: const StadiumBorder(),
        ),
        icon: const Icon(
          CupertinoIcons.arrow_up_right,
          size: 14,
          color: textSecondary,
        ),
        label: Text(
          label,
          style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w600),
        ),
      ),
    );
  }

  // Fades and lifts a result item in, 60ms after the one before it.
  Widget rise(int index, Widget child) {
    final start = 0.35 + index * 0.06;
    final animation = CurvedAnimation(
      parent: reveal,
      curve: Interval(start, math.min(start + 0.4, 1), curve: ease),
    );

    return AnimatedBuilder(
      animation: animation,
      builder: (context, child) => Opacity(
        opacity: animation.value,
        child: Transform.translate(
          offset: Offset(0, (1 - animation.value) * 8),
          child: child,
        ),
      ),
      child: child,
    );
  }
}

// Album cover from a URL, or a plain music note while it loads or if it fails.
class Cover extends StatelessWidget {
  final String url;
  final double iconSize;

  const Cover({super.key, required this.url, this.iconSize = 24});

  @override
  Widget build(BuildContext context) {
    final placeholder = ColoredBox(
      color: surface,
      child: Center(
        child: Icon(CupertinoIcons.music_note, size: iconSize, color: textMuted),
      ),
    );

    return AnimatedSwitcher(
      duration: const Duration(milliseconds: 300),
      child: url.isEmpty
          ? placeholder
          : Image.network(
              url,
              key: ValueKey(url),
              fit: BoxFit.cover,
              width: double.infinity,
              height: double.infinity,
              errorBuilder: (context, error, stack) => placeholder,
            ),
    );
  }
}

// A vinyl record: black grooves with the album cover as the center label.
class Vinyl extends StatelessWidget {
  final double size;
  final String artwork;

  const Vinyl({super.key, required this.size, required this.artwork});

  @override
  Widget build(BuildContext context) {
    final label = size * 0.34;

    return SizedBox(
      width: size,
      height: size,
      child: Stack(
        alignment: Alignment.center,
        children: [
          CustomPaint(size: Size.square(size), painter: VinylPainter()),
          ClipOval(
            child: SizedBox.square(
              dimension: label,
              child: Cover(url: artwork, iconSize: 20),
            ),
          ),
          // Spindle hole.
          Container(
            width: 6,
            height: 6,
            decoration: const BoxDecoration(
              color: Colors.black,
              shape: BoxShape.circle,
            ),
          ),
        ],
      ),
    );
  }
}

class VinylPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    final radius = size.width / 2;

    // Black disc with a faint sheen that turns with the record.
    canvas.drawCircle(center, radius, Paint()..color = const Color(0xFF151517));
    canvas.drawCircle(
      center,
      radius,
      Paint()
        ..shader = const SweepGradient(
          colors: [
            Color(0x00FFFFFF),
            Color(0x26FFFFFF),
            Color(0x00FFFFFF),
            Color(0x00FFFFFF),
            Color(0x26FFFFFF),
            Color(0x00FFFFFF),
          ],
        ).createShader(Rect.fromCircle(center: center, radius: radius)),
    );

    // Grooves.
    final groove = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 0.6;
    for (var r = radius * 0.4; r < radius - 4; r += 3) {
      groove.color = Color(r % 6 < 3 ? 0x1AFFFFFF : 0x0DFFFFFF);
      canvas.drawCircle(center, r, groove);
    }

    // Rim, so the edge reads against the dark page.
    canvas.drawCircle(
      center,
      radius - 0.5,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1
        ..color = const Color(0x24FFFFFF),
    );
  }

  @override
  bool shouldRepaint(VinylPainter oldDelegate) => false;
}

// Progress ring around the listen button, plus rings spreading out while
// listening. They only move while the app is actually listening.
class ListenRingsPainter extends CustomPainter {
  final double spread; // 0-1, loops while listening
  final double progress; // 0-1, how far through listening
  final bool active;

  ListenRingsPainter({
    required this.spread,
    required this.progress,
    required this.active,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    if (!active) return;

    // Three rings, evenly spaced in time, fading as they grow.
    for (var k = 0; k < 3; k++) {
      final p = (spread + k / 3) % 1;
      canvas.drawCircle(
        center,
        98 + p * 22,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1.5
          ..color = accent.withValues(alpha: (1 - p) * 0.4),
      );
    }

    // Progress track and arc.
    final rect = Rect.fromCircle(center: center, radius: 90);
    canvas.drawCircle(
      center,
      90,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 3
        ..color = hairline,
    );
    canvas.drawArc(
      rect,
      -math.pi / 2,
      progress * 2 * math.pi,
      false,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 3
        ..strokeCap = StrokeCap.round
        ..color = accent,
    );
  }

  @override
  bool shouldRepaint(ListenRingsPainter old) =>
      old.spread != spread || old.progress != progress || old.active != active;
}

// Small equalizer bars that move while sound is live (listening or playing).
class LiveBars extends StatefulWidget {
  final int count;
  final double height;
  final double barWidth;
  final Color color;

  const LiveBars({
    super.key,
    this.count = 3,
    this.height = 12,
    this.barWidth = 2,
    this.color = accent,
  });

  @override
  State<LiveBars> createState() => _LiveBarsState();
}

class _LiveBarsState extends State<LiveBars>
    with SingleTickerProviderStateMixin {
  late final AnimationController wave = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 1400),
  )..repeat();

  // Whole-number speeds so the loop is seamless.
  static const speeds = [1, 2, 1, 3, 2];
  static const phases = [0.0, 1.2, 2.4, 0.6, 1.8];

  @override
  void dispose() {
    wave.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: wave,
      builder: (context, _) => SizedBox(
        height: widget.height,
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: List.generate(widget.count, (i) {
            final t = 2 * math.pi * wave.value * speeds[i % 5] + phases[i % 5];
            final level = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(t));
            return Container(
              width: widget.barWidth,
              height: widget.height * level,
              margin: EdgeInsets.symmetric(horizontal: widget.barWidth / 2),
              decoration: BoxDecoration(
                color: widget.color,
                borderRadius: BorderRadius.circular(widget.barWidth / 2),
              ),
            );
          }),
        ),
      ),
    );
  }
}
