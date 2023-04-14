# Copyright (c) 2023, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import torch

from nemo.collections.tts.inference.spectrogram_synthesizers import FastPitchSpectrogramSynthesizer
from nemo.collections.tts.models import FastPitchModel


class TestSpectrogramSynthesizers:

    @pytest.fixture
    def spec_synthesizer(self):
        fastpitch_model = FastPitchModel.from_pretrained("tts_en_fastpitch_multispeaker").eval().to("cpu")
        spec_synthesizer = FastPitchSpectrogramSynthesizer(model=fastpitch_model)
        return spec_synthesizer

    @pytest.mark.nightly
    @pytest.mark.with_downloads
    @pytest.mark.run_only_on("CPU")
    @pytest.mark.unit
    def test_synthesize_spectrogram(self, spec_synthesizer):
        batch_size = 2
        text_length = 10
        spec_dim = 80
        tokens = torch.zeros([batch_size, text_length], dtype=torch.int32, device="cpu")
        speaker = torch.randint(low=0, high=10, size=[batch_size], dtype=torch.int32, device="cpu")
        pitch = torch.rand([batch_size, text_length]).to("cpu")
        pace = torch.FloatTensor(1).uniform_(0.5, 1.5).to("cpu")
        spec = spec_synthesizer.synthesize_spectrogram(tokens=tokens, speaker=speaker, pitch=pitch, pace=pace)

        assert len(spec.shape) == 3
        assert spec.shape[0] == batch_size
        assert spec.shape[1] == spec_dim
        assert spec.shape[2] > text_length
