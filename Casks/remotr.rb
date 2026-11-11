cask "remotr" do
  version "1.0.53"
  sha256 "b85523530b24d8908bebea26611429a300712d00687b59752a4a28adc535a601"

  url "https://download.ducky.build/p/62810754-7260-44e3-b3e1-3b67d378bb1b/Remotr-v#{version}.dmg"
  name "Remotr"
  desc "Remote desktop server using RDP"
  homepage "https://remotr.app/"

  livecheck do
    url "https://remotr.app/appcast.xml"
    strategy :sparkle, &:short_version
  end

  auto_updates true
  depends_on macos: :ventura

  app "Remotr.app"
end
