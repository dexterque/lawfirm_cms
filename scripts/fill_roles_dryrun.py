#!/usr/bin/env python
import os
import sys
import csv

# Ensure project root is on path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.dev')
import django
django.setup()

from team.models import TeamMemberPage

ROLE_LABELS = {
    'host': '主办律师',
    'chief_assistant': '律师主任助理',
    'business_assistant': '律师业务助理',
}


def suggest_role_for_member(m):
    # If already has role, keep it (mark as already_set)
    if getattr(m, 'role', None):
        return m.role, 'already_set'
    pos = (m.position or '').strip()
    lowered = pos.lower()
    if '主办' in lowered or '主办律师' in lowered:
        return 'host', 'matched_position'
    if '主任助理' in lowered or '主任' in lowered:
        return 'chief_assistant', 'matched_position'
    if '业务助理' in lowered or '助理' in lowered:
        return 'business_assistant', 'matched_position'
    return '', 'no_match'


def main():
    members = TeamMemberPage.objects.live().order_by('first_published_at')
    results = []
    for m in members:
        suggested, reason = suggest_role_for_member(m)
        results.append({
            'id': m.id,
            'title': m.title,
            'position': m.position or '',
            'current_role': getattr(m, 'role', '') or '',
            'suggested_role': suggested,
            'suggested_label': ROLE_LABELS.get(suggested, ''),
            'reason': reason,
        })

    # Print summary
    total = len(results)
    already = len([r for r in results if r['reason'] == 'already_set'])
    matched = len([r for r in results if r['reason'] == 'matched_position'])
    nomatch = len([r for r in results if r['reason'] == 'no_match'])

    print('\nDry-run role mapping results')
    print('Total members:', total)
    print('Already have role:', already)
    print('Matched by position:', matched)
    print('No match:', nomatch)

    # Write CSV for review
    out_csv = os.path.join(SCRIPT_DIR, 'fill_roles_dryrun_results.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'title', 'position', 'current_role', 'suggested_role', 'suggested_label', 'reason'])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print('\nDetailed results saved to:', out_csv)
    print('\nSample suggestions:')
    for r in results[:50]:
        sug = r['suggested_label'] or '-' 
        cur = r['current_role'] or '-'
        print(f"[{r['id']}] {r['title']!s:30} | position: {r['position']!s:20} | current: {cur:20} | suggested: {sug:20} | reason: {r['reason']}")


if __name__ == '__main__':
    main()
