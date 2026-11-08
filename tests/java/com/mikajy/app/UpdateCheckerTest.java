package com.mikajy.app;

import org.json.JSONObject;

/** Plain-Java checks for the update answer parser and the release-URL guard (no Android needed). */
public final class UpdateCheckerTest {
  private static final String R = UpdateChecker.RELEASES;
  private static int failures;

  private static void check(boolean condition, String what) {
    if (!condition) { failures++; System.err.println("FAIL: " + what); }
  }

  private static String release(String tag, String htmlUrl, String apkUrl, boolean prerelease) {
    return "{\"tag_name\":\"" + tag + "\",\"html_url\":\"" + htmlUrl + "\",\"draft\":false,\"prerelease\":" + prerelease
        + ",\"assets\":[{\"name\":\"SHA256SUMS.txt\",\"browser_download_url\":\"" + R + "download/" + tag + "/SHA256SUMS.txt\"},"
        + "{\"name\":\"Mikajy-Max.apk\",\"browser_download_url\":\"" + apkUrl + "\"}]}";
  }

  public static void main(String[] args) throws Exception {
    JSONObject ok = new JSONObject(UpdateChecker.parse(release("max-v6.1", R + "tag/max-v6.1", R + "download/max-v6.1/Mikajy-Max-6.1.apk", true)));
    check(ok.getBoolean("ok") && "max-v6.1".equals(ok.getString("tag")), "a Max pre-release is accepted (that is how Max is published)");
    check((R + "download/max-v6.1/Mikajy-Max-6.1.apk").equals(ok.getString("apk")), "apk link picked");
    check((R + "tag/max-v6.1").equals(ok.getString("url")), "page link kept");

    JSONObject foreign = new JSONObject(UpdateChecker.parse(release("max-v6.1", "https://evil.example/x", "https://evil.example/a.apk", true)));
    check(foreign.getBoolean("ok") && R.equals(foreign.getString("url")) && foreign.getString("apk").isEmpty(), "foreign links are replaced");

    // Plain Mikajy's tags (v5.1) and malformed tags are never offered to Max.
    for (String bad : new String[] {"latest", "v5.1", "max-v6", "max-v6.x", "6.1", "max-6.1", "max-v6.1.2.3", "max-v1.2<script>", "xmax-v6.1"}) {
      check(!new JSONObject(UpdateChecker.parse(release(bad, R + "x", R + "y.apk", true))).getBoolean("ok"), "tag rejected: " + bad);
    }
    check(!new JSONObject(UpdateChecker.parse(release("max-v6.1", R + "x", R + "y.apk", true).replace("\"draft\":false", "\"draft\":true"))).getBoolean("ok"), "draft ignored");

    // GitHub's list: newest first; Mikajy releases and drafts in between are skipped, the first Max release wins.
    String list = "[" + release("v5.0", R + "tag/v5.0", R + "download/v5.0/Mikajy-5.0.apk", false) + ","
        + release("max-v6.2", R + "tag/max-v6.2", R + "download/max-v6.2/Mikajy-Max-6.2.apk", true) + ","
        + release("max-v6.1", R + "tag/max-v6.1", R + "download/max-v6.1/Mikajy-Max-6.1.apk", true) + "]";
    JSONObject pick = new JSONObject(UpdateChecker.parse(list));
    check(pick.getBoolean("ok") && "max-v6.2".equals(pick.getString("tag")), "list: first Max release wins, plain Mikajy releases skipped");
    check(!new JSONObject(UpdateChecker.parse("[" + release("v5.0", R + "x", R + "y.apk", false) + "]")).getBoolean("ok"), "list without a Max release -> error");
    check(!new JSONObject(UpdateChecker.parse("[]")).getBoolean("ok"), "empty list -> error");
    check(!new JSONObject(UpdateChecker.parse("not json")).getBoolean("ok"), "garbage rejected");
    check(!new JSONObject(UpdateChecker.parse("{}")).getBoolean("ok"), "empty object rejected");

    check(UpdateChecker.isReleaseUrl(R + "tag/v5.1"), "release url accepted");
    check(!UpdateChecker.isReleaseUrl(null), "null refused");
    check(!UpdateChecker.isReleaseUrl("http://github.com/ARHeritiana/Mikajy/releases/x"), "plain http refused");
    check(!UpdateChecker.isReleaseUrl("https://github.com/ARHeritiana/Mikajy-evil/releases/x"), "look-alike repo refused");
    check(!UpdateChecker.isReleaseUrl(R + "../../../evil"), "path traversal refused");
    check(!UpdateChecker.isReleaseUrl("file:///sdcard/x"), "file url refused");
    check(!UpdateChecker.isReleaseUrl("intent://x#Intent;end"), "intent url refused");

    if (failures > 0) { System.err.println(failures + " failure(s)"); System.exit(1); }
    System.out.println("UpdateChecker: all checks passed");
  }
}
