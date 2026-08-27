#!/usr/bin/env python3
"""H.264 encoder with an actual bitrate control.

avconvert only takes named presets, and its lowest useful one still wrote 38MB
for 69 seconds of motion graphics — fine for a master, useless on a web page.
This drives AVAssetReader/AVAssetWriter directly so the bitrate can be set,
scales to a target width, and drops audio (every clip on the site plays muted).
"""
import time

from Quartz import kCVPixelBufferPixelFormatTypeKey, kCVPixelFormatType_32BGRA
from AVFoundation import (
    AVAssetReader, AVAssetReaderTrackOutput, AVAssetWriter, AVAssetWriterInput,
    AVURLAsset, AVMediaTypeVideo, AVFileTypeMPEG4,
    AVVideoCodecKey, AVVideoWidthKey, AVVideoHeightKey,
    AVVideoCompressionPropertiesKey, AVVideoAverageBitRateKey,
    AVVideoMaxKeyFrameIntervalKey, AVVideoProfileLevelKey,
    AVVideoProfileLevelH264HighAutoLevel, AVVideoScalingModeKey,
    AVVideoScalingModeResizeAspect,
)
from CoreMedia import CMTimeMakeWithSeconds, CMTimeRangeMake
from Foundation import NSURL, NSDictionary


def encode(src, dest, width=1280, kbps=1400, start=0.0, duration=None):
    """Transcode `src` to H.264 MP4 at `width` and roughly `kbps`."""
    asset = AVURLAsset.URLAssetWithURL_options_(NSURL.fileURLWithPath_(src), None)
    track = asset.tracksWithMediaType_(AVMediaTypeVideo)[0]
    size = track.naturalSize()
    w = int(width)
    h = int(round(size.height * width / size.width))
    h -= h % 2                                    # H.264 wants even dimensions

    reader = AVAssetReader.assetReaderWithAsset_error_(asset, None)[0]
    if duration is not None:
        reader.setTimeRange_(CMTimeRangeMake(
            CMTimeMakeWithSeconds(start, 600),
            CMTimeMakeWithSeconds(duration, 600)))
    out = AVAssetReaderTrackOutput.assetReaderTrackOutputWithTrack_outputSettings_(
        track, NSDictionary.dictionaryWithObject_forKey_(
            kCVPixelFormatType_32BGRA, kCVPixelBufferPixelFormatTypeKey))
    out.setAlwaysCopiesSampleData_(False)
    reader.addOutput_(out)

    url = NSURL.fileURLWithPath_(dest)
    writer = AVAssetWriter.assetWriterWithURL_fileType_error_(url, AVFileTypeMPEG4, None)[0]
    settings = {
        AVVideoCodecKey: "avc1",
        AVVideoWidthKey: w,
        AVVideoHeightKey: h,
        AVVideoScalingModeKey: AVVideoScalingModeResizeAspect,
        AVVideoCompressionPropertiesKey: {
            AVVideoAverageBitRateKey: int(kbps * 1000),
            AVVideoMaxKeyFrameIntervalKey: 60,
            AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        },
    }
    vin = AVAssetWriterInput.assetWriterInputWithMediaType_outputSettings_(
        AVMediaTypeVideo, settings)
    vin.setExpectsMediaDataInRealTime_(False)
    vin.setTransform_(track.preferredTransform())
    writer.addInput_(vin)

    writer.startWriting()
    # Map the trim point to time zero in the output. Starting the session at
    # kCMTimeZero instead leaves the samples carrying their original
    # timestamps, and a clip trimmed from 190s writes a file that claims to be
    # 230s long and will not open.
    writer.startSessionAtSourceTime_(CMTimeMakeWithSeconds(start, 600))
    reader.startReading()

    while True:
        if not vin.isReadyForMoreMediaData():
            time.sleep(0.005)
            continue
        buf = out.copyNextSampleBuffer()
        if buf is None:
            break
        vin.appendSampleBuffer_(buf)

    vin.markAsFinished()
    done = []
    writer.finishWritingWithCompletionHandler_(lambda: done.append(True))
    while not done and writer.status() == 1:       # 1 = writing
        time.sleep(0.02)
    reader.cancelReading()
    if writer.status() != 2:                       # 2 = completed
        raise RuntimeError(f"encode failed: {writer.error()}")
    return dest
