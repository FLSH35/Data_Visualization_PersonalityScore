import 'dart:io';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;

void main() async {
  // Paths
  const inputPdf = "Input_Certificate.pdf";
  const overlayPdf = "Text_Overlay.pdf";
  const outputPdf = "Updated_Certificate.pdf";
  const sortsMillGoudyFontPath = "SortsMillGoudy-Italic.ttf";
  const alexBrushFontPath = "AlexBrush-Regular.ttf";

  // Define text and their positions
  final texts = [
    {"text": "Adventurer", "font": "SortsMillGoudy", "size": 53.0, "position": [217.66, 428.03]},
    {"text": "Frank", "font": "AlexBrush", "size": 80.0, "position": [272.11, 335.97]}
  ];

  try {
    // Step 1: Create Text Overlay PDF
    await createTextOverlay(overlayPdf, texts, sortsMillGoudyFontPath, alexBrushFontPath);

    // Step 2: Merge PDFs
    await mergePdfs(inputPdf, overlayPdf, outputPdf);

    print("Updated certificate saved to $outputPdf");
  } catch (e) {
    print("An error occurred: $e");
  }
}

Future<void> createTextOverlay(
  String outputPath,
  List<Map<String, dynamic>> texts,
  String sortsMillGoudyFontPath,
  String alexBrushFontPath,
) async {
  final pdf = pw.Document();

  // Load fonts
  final sortsMillGoudyFont = pw.Font.ttf(await File(sortsMillGoudyFontPath).readAsBytes());
  final alexBrushFont = pw.Font.ttf(await File(alexBrushFontPath).readAsBytes());

  // Get page dimensions (hardcoded for simplicity; match your input PDF's size if known)
  final pageWidth = 595.28; // A4 width in points
  final pageHeight = 841.89; // A4 height in points

  pdf.addPage(
    pw.Page(
      pageFormat: PdfPageFormat(pageWidth, pageHeight),
      build: (pw.Context context) {
        return pw.Stack(
          children: texts.map((textData) {
            final font = textData["font"] == "SortsMillGoudy" ? sortsMillGoudyFont : alexBrushFont;
            final position = textData["position"] as List<double>;
            return pw.Positioned(
              left: position[0],
              top: pageHeight - position[1], // Flip y-axis for PDF coordinates
              child: pw.Text(
                textData["text"],
                style: pw.TextStyle(font: font, fontSize: textData["size"] as double),
              ),
            );
          }).toList(),
        );
      },
    ),
  );

  // Save overlay PDF
  final file = File(outputPath);
  await file.writeAsBytes(await pdf.save());
}

Future<void> mergePdfs(String inputPdfPath, String overlayPdfPath, String outputPdfPath) async {
  final inputPdf = await File(inputPdfPath).readAsBytes();
  final overlayPdf = await File(overlayPdfPath).readAsBytes();

  final pdfDoc = pw.Document();
  final inputDoc = pw.Document.fromBytes(inputPdf);
  final overlayDoc = pw.Document.fromBytes(overlayPdf);

  for (var i = 0; i < inputDoc.pages.length; i++) {
    final inputPage = inputDoc.pages[i];
    final overlayPage = i < overlayDoc.pages.length ? overlayDoc.pages[i] : null;

    pdfDoc.addPage(
      pw.Page(
        pageFormat: inputPage.pageFormat,
        build: (pw.Context context) {
          return pw.Stack(
            children: [
              pw.FullPage(ignoreMargins: true, child: pw.Image(inputPage.createImage())),
              if (overlayPage != null)
                pw.FullPage(ignoreMargins: true, child: pw.Image(overlayPage.createImage())),
            ],
          );
        },
      ),
    );
  }

  final mergedFile = File(outputPdfPath);
  await mergedFile.writeAsBytes(await pdfDoc.save());
}
